#!/usr/bin/env python3
"""Structural lint for the eval seed set — Python 3 stdlib only.

This is NOT an eval *runner*: it never calls a model and never executes a skill.
It only guards the *structure* of the manually-authored `evals/<skill>/cases.md`
corpus so capability-expansion edits cannot silently rot it. Two guards:

  1. Presence + parseability: every skill (a subdir of a phase dir) has a
     `cases.md`; every case object carries the required keys; every
     `target_skill` names a real skill slug.
  2. No-dropped-skill regression: the committed `evals/structure-manifest.json`
     records the structural facts (skill list, count, required keys). A skill
     that had a cases.md and lost it fails the run.

The manifest stores ONLY structural facts (never output scores) — a key
allowlist is enforced so it can never quietly grow into the rejected
"output-score baseline" runner.

Usage:
  python3 scripts/check-evals.py            # lint + compare to manifest (CI gate; exit 1 on fail)
  python3 scripts/check-evals.py --update    # regenerate the manifest after an intentional change
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVALS = os.path.join(ROOT, "evals")
MANIFEST = os.path.join(EVALS, "structure-manifest.json")
ROUTING_LIBRARY = os.path.join(ROOT, "references", "auto-routing-scenarios.md")

PHASE_DIRS = [
    "seo-geo/research", "seo-geo/build", "seo-geo/optimize", "seo-geo/monitor", "protocol",   # SEO/GEO
    "influencer/discover", "influencer/plan", "influencer/activate", "influencer/measure",      # influencer (4x4)
    "ad/research", "ad/orchestrate", "ad/activate", "ad/scale",                                                        # paid ads (when present)
    "email/setup", "email/engage", "email/nurture", "email/deliver",                                                          # email marketing
    "launch/research", "launch/assemble", "launch/mobilize", "launch/prove",                                                  # product launch (RAMP)
    "social/explore", "social/craft", "social/host", "social/observe",                                                        # organic social (ECHO)
    "narrative/trace", "narrative/architect", "narrative/land", "narrative/evaluate",                                          # brand narrative (TALE)
]
REQUIRED_CASE_KEYS = [
    "id", "type", "target_skill", "scenario",
    "input_summary", "expected_behavior", "failure_modes",
]
# Manifest may carry ONLY these keys. Anything matching a score/metric word is a
# scope-creep attempt (the rejected output-score baseline) and fails the run.
MANIFEST_ALLOWED_KEYS = {"skills", "count", "required_case_keys", "note"}
SCORE_WORD = re.compile(r"score|rating|cvi|rqs|pass[_-]?rate|metric|baseline_score", re.I)

# Each case is a single-line flow object (optionally a `- ` list item). Line-based
# extraction (first `{` to last `}` on the line) so inner braces like /blog/{slug}
# inside a case do not confuse detection.
CASE_LINE = re.compile(r"^\s*-?\s*(\{.*\})\s*$")
# target_skill is quoted in the routing library ("skill-name") and bare in
# evals/*/cases.md (skill-name) — tolerate both.
TARGET_SKILL_RE = re.compile(r'target_skill:\s*"?([A-Za-z0-9_-]+)"?')
# expected_route is a quoted chain like "/aaron-marketing:ad --phase activate -> ...".
EXPECTED_ROUTE_RE = re.compile(r'expected_route:\s*"([^"]*)"')
ROUTE_CMD_RE = re.compile(r'/aaron-marketing:([a-z-]+)(?:\s+--(mode|phase)\s+([a-z-]+))?')
# Each command's valid selector: SEO/GEO uses --mode, the six others --phase,
# auto takes neither (only --deep). Guards expected_route against a typo'd command
# or an invalid/mismatched phase|mode value (e.g. "ad --mode research").
COMMAND_MODES = {
    "seo-geo": ("mode", {"research", "create", "audit", "track"}),
    "influencer": ("phase", {"discover", "plan", "activate", "measure"}),
    "ad": ("phase", {"research", "orchestrate", "activate", "scale"}),
    "email": ("phase", {"setup", "engage", "nurture", "deliver"}),
    "launch": ("phase", {"research", "assemble", "mobilize", "prove"}),
    "social": ("phase", {"explore", "craft", "host", "observe"}),
    "narrative": ("phase", {"trace", "architect", "land", "evaluate"}),
    "auto": (None, set()),
}

fails = []
def fail(msg):
    fails.append(msg)
    print("FAIL  " + msg)


def discover_skills():
    """Return sorted list of skill slugs = subdirs of existing phase dirs."""
    slugs = []
    for p in PHASE_DIRS:
        d = os.path.join(ROOT, p)
        if not os.path.isdir(d):
            continue
        for name in os.listdir(d):
            if os.path.isfile(os.path.join(d, name, "SKILL.md")):
                slugs.append(name)
    return sorted(set(slugs))


def lint_cases(slug):
    """Lint one skill's cases.md; return True if a cases.md exists (for presence)."""
    path = os.path.join(EVALS, slug, "cases.md")
    if not os.path.isfile(path):
        return False
    text = open(path, encoding="utf-8").read()
    objs = [m.group(1) for line in text.splitlines()
            for m in (CASE_LINE.match(line),) if m]
    if not objs:
        fail("%s/cases.md has no parseable case objects" % slug)
        return True
    for i, obj in enumerate(objs, 1):
        for key in REQUIRED_CASE_KEYS:
            # Match the key only at a key POSITION: line start, or right after '{'
            # or ',' (with optional whitespace), optionally quoted, then ':'. Using
            # '{' / ',' as the boundary (NOT bare \s) means a space-preceded '<key>:'
            # inside a quoted prose value no longer masks a truly-missing key.
            if not re.search(r'(?:^|[{,])\s*"?' + re.escape(key) + r'"?\s*:', obj):
                fail("%s/cases.md case #%d missing required key '%s'" % (slug, i, key))
        m = re.search(r"target_skill:\s*([A-Za-z0-9_-]+)", obj)
        if m and m.group(1) not in VALID_SLUGS:
            fail("%s/cases.md case #%d target_skill '%s' is not a real skill" % (slug, i, m.group(1)))
    return True


VALID_SLUGS = set(discover_skills())


def lint_routing_library():
    """Guard the /aaron-marketing:auto routing library against skill-rename drift.

    references/auto-routing-scenarios.md is a SECOND place that names skills by
    slug (target_skill). check-evals otherwise only lints evals/<slug>/cases.md,
    so a renamed or deleted skill used to leave a dangling routing target with NO
    CI failure — the same drift class that once silently froze the library at the
    v12 four-discipline era. Assert every target_skill in the library resolves to
    a real skill. (Per-discipline coverage is guarded separately by
    check-versions.sh; this guards slug validity.)
    """
    if not os.path.isfile(ROUTING_LIBRARY):
        fail("references/auto-routing-scenarios.md missing — the /aaron-marketing:auto routing library")
        return
    text = open(ROUTING_LIBRARY, encoding="utf-8").read()
    seen = 0
    for i, line in enumerate(text.splitlines(), 1):
        if not CASE_LINE.match(line):
            continue
        m = TARGET_SKILL_RE.search(line)
        if not m:
            fail("auto-routing-scenarios.md line %d: routing case has no target_skill" % i)
            continue
        seen += 1
        if m.group(1) not in VALID_SLUGS:
            fail("auto-routing-scenarios.md line %d: target_skill '%s' is not a real skill"
                 % (i, m.group(1)))
        er = EXPECTED_ROUTE_RE.search(line)
        if er:
            for mm in ROUTE_CMD_RE.finditer(er.group(1)):
                cmd, flag, val = mm.group(1), mm.group(2), mm.group(3)
                spec = COMMAND_MODES.get(cmd)
                if spec is None:
                    fail("auto-routing-scenarios.md line %d: expected_route names unknown "
                         "command '/aaron-marketing:%s'" % (i, cmd))
                    continue
                exp_flag, allowed = spec
                if flag and (flag != exp_flag or val not in allowed):
                    fail("auto-routing-scenarios.md line %d: expected_route '--%s %s' is not "
                         "valid for /aaron-marketing:%s" % (i, flag, val, cmd))
    print("== routing-library lint: %d routing cases, target_skill + expected_route checked ==" % seen)


def build_manifest():
    return {
        "skills": sorted(VALID_SLUGS),
        "count": len(VALID_SLUGS),
        "required_case_keys": REQUIRED_CASE_KEYS,
        "note": "Structural facts only — never output scores. Regenerate with check-evals.py --update.",
    }


def main():
    update = "--update" in sys.argv

    present = [s for s in sorted(VALID_SLUGS) if lint_cases(s)]
    missing = sorted(set(VALID_SLUGS) - set(present))
    for s in missing:
        fail("skill '%s' has no evals/%s/cases.md (presence gate)" % (s, s))

    print("== eval structural lint: %d skills, %d with cases.md ==" % (len(VALID_SLUGS), len(present)))

    lint_routing_library()

    if update:
        # Fail CLOSED: never write the regression baseline from a failing lint —
        # that would bake the current breakage in as the new "expected" structure.
        if fails:
            print("\nREFUSING to write structure-manifest.json — fix the %d lint "
                  "issue(s) above first." % len(fails))
            return 1
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(build_manifest(), f, indent=2, ensure_ascii=False)
            f.write("\n")
        print("wrote %s (%d skills)" % (os.path.relpath(MANIFEST, ROOT), len(VALID_SLUGS)))
        return 0

    if os.path.isfile(MANIFEST):
        try:
            man = json.load(open(MANIFEST, encoding="utf-8"))
        except (ValueError, OSError) as e:
            fail("structure-manifest.json is unreadable/corrupt: %s" % e)
            man = {}
        stray = [k for k in man if k not in MANIFEST_ALLOWED_KEYS or SCORE_WORD.search(k)]
        if stray:
            fail("manifest has disallowed/score-like keys (scope creep): %s" % stray)
        for s in man.get("skills", []):
            if s not in present:
                fail("manifest skill '%s' lost its cases.md (regression)" % s)
        if man.get("required_case_keys") != REQUIRED_CASE_KEYS:
            fail("manifest required_case_keys drifted from the script — re-run --update")
        if man.get("count") != len(man.get("skills", [])):
            fail("manifest count (%s) != its skills list length (%d) — re-run --update"
                 % (man.get("count"), len(man.get("skills", []))))
        print("== compared against structure-manifest.json (%d skills) ==" % len(man.get("skills", [])))
    else:
        print("NOTE: no structure-manifest.json yet — run with --update to create it.")

    if fails:
        print("\nEVAL STRUCTURE LINT FAILED — %d issue(s)." % len(fails))
        return 1
    print("\nAll eval structural-lint checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
