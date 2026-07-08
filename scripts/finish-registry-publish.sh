#!/usr/bin/env bash
# finish-registry-publish.sh — resumable, rate-limit-respecting trickle to finish
# the ClawHub + SkillHub publish tail after a bulk run hit platform rate limits.
#
# Resumable: records successes in a state file so re-runs skip them. The queue
# is the known rate-limited tail; verify live registry dashboards before using
# --live if the public counts may have moved.
#
# Platform limits it respects:
#   ClawHub  — ~5 NEW skills / hour (hard). This script publishes 1 every 13 min
#              (≈4-5/hour) so it stays under the cap. ~5 skills ≈ 1 hour.
#   SkillHub — burst limit (发布频率过高). Publishes 1 every 40s; on a 429 it backs
#              off 5 min then retries the same skill. ~21 skills ≈ 15-20 min once cool.
#
# Prereqs (already satisfied on the owner's machine): `clawhub whoami` = aaron-he-zhu,
# `skillhub auth whoami` returns a userId. Re-login if either has expired.
#
# Usage:
#   bash scripts/finish-registry-publish.sh                  # dry-run, both platforms
#   bash scripts/finish-registry-publish.sh skillhub          # dry-run, SkillHub tail only
#   bash scripts/finish-registry-publish.sh --live skillhub   # publish SkillHub tail
#   bash scripts/finish-registry-publish.sh --live clawhub    # publish ClawHub tail
set -u
cd "$(cd "$(dirname "$0")/.." && pwd)"
STATE="${TMPDIR:-/tmp}/finish-registry-publish.state"
LIVE=0
TARGET="both"
while [ $# -gt 0 ]; do
  case "$1" in
    --live) LIVE=1 ;;
    clawhub|skillhub|both) TARGET="$1" ;;
    *) echo "usage: $0 [--live] [clawhub|skillhub|both]"; exit 1 ;;
  esac
  shift
done
touch "$STATE"
done_already() { grep -qxF "$1" "$STATE"; }
mark_done()    { echo "$1" >> "$STATE"; }

CLAW_TAIL="narrative-cascade-planner narrative-enablement-kit proof-point-packager message-test-designer narrative-resonance-monitor"
SKILL_TAIL="entity-optimizer creator-registry offer-claims-registry consent-registry launch-registry channel-registry memory-management narrative-registry brand-language-codifier message-system-architect strategic-narrative-designer positioning-truth-tracer story-bank-builder narrative-quality-auditor narrative-drift-monitor narrative-resonance-monitor message-test-designer pitch-narrative-builder narrative-cascade-planner narrative-enablement-kit proof-point-packager"

dir_for() {
  python3 -c "import json,sys; s=sys.argv[1]; p=next((x for x in json.load(open('.claude-plugin/plugin.json'))['skills'] if x.endswith('/'+s)), ''); print(p[2:] if p.startswith('./') else p, end='')" "$1"
}

publish_clawhub() {
  echo "== ClawHub tail (1 / 13 min to stay under 5/hour) =="
  for s in $CLAW_TAIL; do
    done_already "clawhub:$s" && { echo "  skip $s (done)"; continue; }
    if [ "$LIVE" -eq 0 ]; then
      echo "  would publish $s (dry-run)"
      continue
    fi
    ok=0
    for try in 1 2 3; do
      # Key success off publish-clawhub.sh's exit code (0 = published OR the idempotent
      # "already on ClawHub" path), not a literal string it never prints. Only the hourly
      # new-skill cap is worth waiting 13 min for; break on any other (hard) error so a
      # genuine failure doesn't burn ~39 min of retries.
      out=$(bash scripts/publish-clawhub.sh --i-accept-mit0 --skill "$s" 2>&1); rc=$?
      if [ "$rc" -eq 0 ]; then echo "  OK $s"; mark_done "clawhub:$s"; ok=1; break; fi
      if echo "$out" | grep -qiE 'RateLimit|reset in|too many|rate.?limit'; then
        echo "  rate-limited $s (try $try) — waiting 13 min for the hourly window"; sleep 780
      else
        echo "  FAILED $s (non-rate-limit error) — not retrying:"; echo "$out" | tail -3; break
      fi
    done
    [ $ok -eq 0 ] && echo "  STILL-FAILED $s (rerun later)"
    [ $ok -eq 1 ] && sleep 780
  done
}

publish_skillhub() {
  echo "== SkillHub tail (1 / 40s; 5-min backoff on 429) =="
  for s in $SKILL_TAIL; do
    done_already "skillhub:$s" && { echo "  skip $s (done)"; continue; }
    dir=$(dir_for "$s"); [ -z "$dir" ] && { echo "  NODIR $s"; continue; }
    if [ "$LIVE" -eq 0 ]; then
      echo "  would publish $s -> $dir (dry-run)"
      continue
    fi
    ok=0
    for try in 1 2 3 4; do
      # Success = the CLI's exit code, with the output string as a fallback signal.
      out=$(skillhub publish "$dir" --host https://api.skillhub.cn 2>&1); rc=$?
      if [ "$rc" -eq 0 ] || echo "$out" | grep -qE 'Published|skillId'; then echo "  OK $s"; mark_done "skillhub:$s"; ok=1; break; fi
      echo "  rate-limited $s (try $try) — backing off 5 min"; sleep 300
    done
    [ $ok -eq 0 ] && echo "  STILL-FAILED $s (rerun later)"
    sleep 40
  done
}

case "$TARGET" in
  clawhub)  publish_clawhub ;;
  skillhub) publish_skillhub ;;
  both)     publish_skillhub; publish_clawhub ;;
  *) echo "usage: $0 [clawhub|skillhub|both]"; exit 1 ;;
esac
echo "done — state at $STATE (delete to force replay of locally marked successes)"
