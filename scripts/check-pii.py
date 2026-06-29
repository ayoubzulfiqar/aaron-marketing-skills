#!/usr/bin/env python3
"""PII / secret scanner — Python 3 stdlib only.

Ported (the detection half only) from common pre-commit secret scanners; the
vendor-attribution / CTA-block half is deliberately NOT included. Fails closed
on high-confidence secrets and non-allowlisted emails so credentials can't be
committed into this public skill library.

Scans tracked text files. Phone/IPv4 detection is intentionally omitted — a
content/SEO repo is full of numbers and they produce false positives.

Usage:
  python3 scripts/check-pii.py                 # scan the repo (CI gate; exit 1 on finding)
  python3 scripts/check-pii.py path [path ...] # scan specific paths
"""
from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCAN_EXTS = {".md", ".py", ".sh", ".json", ".yml", ".yaml", ".txt", ".js", ".ts"}
SKIP_DIRS = {".git", "reference-oss", "node_modules", "__pycache__", ".agents", ".claude"}

# High-confidence secret patterns (name, regex).
PATTERNS = [
    ("OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{30,}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Bearer token", re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{24,}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("URL-embedded credentials", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^/\s:@]+:[^/\s:@]+@")),
    ("US SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
]

EMAIL = re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
# Allowlisted email domains / fragments (placeholders, project-public, doc examples).
EMAIL_ALLOW = ("example.com", "example.org", "example.net", "anthropic.com",
               "noreply", "your-domain", "yourdomain", "user@", "test@", "name@", "you@",
               "zhuhe.io")  # project's intentional public contact address
# Generic allowlist fragments that neutralize an otherwise-matching line.
LINE_ALLOW = ("555-", "xxxx", "redacted", "placeholder", "AKIAIOSFODNN7EXAMPLE")


def scan_file(path):
    findings = []
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return findings
    for n, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if any(a in low for a in LINE_ALLOW):
            continue
        for name, pat in PATTERNS:
            if pat.search(line):
                findings.append((n, name, line.strip()[:120]))
        for m in EMAIL.finditer(line):
            email = m.group(0)
            if not any(a in email.lower() for a in EMAIL_ALLOW):
                findings.append((n, "email address", email))
    return findings


def iter_targets(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
            continue
        for dirpath, dirnames, filenames in os.walk(p):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in filenames:
                if os.path.splitext(fn)[1].lower() in SCAN_EXTS:
                    yield os.path.join(dirpath, fn)


def main():
    paths = sys.argv[1:] or [ROOT]
    total = 0
    for f in iter_targets(paths):
        for n, name, snippet in scan_file(f):
            total += 1
            print("FAIL  %s:%d  %s  ::  %s" % (os.path.relpath(f, ROOT), n, name, snippet))
    if total:
        print("\nPII/SECRET SCAN FAILED — %d finding(s). Redact or add to the allowlist if a false positive." % total)
        return 1
    print("PII/secret scan clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
