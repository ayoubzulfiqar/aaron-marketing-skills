#!/usr/bin/env bash
# Dependency-creep guard — the moat protector.
#
# This project's contract: the ONLY allowed code is the bash validator + Python
# *stdlib-only* connector/check helpers. No pip / third-party deps, ever. This
# guard fails closed if any script under scripts/ imports a denylisted package,
# so a borrowed helper (trend-scout, dossier, atom-extraction, ROAS math, ...)
# can never quietly pull numpy/pandas/requests/whisper/etc.
#
# Run: bash scripts/check-stdlib-only.sh   (exit 0 = clean, 1 = violation)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Packages that are NOT in the Python standard library.
DENY='numpy|pandas|scipy|sklearn|scikit|requests|httpx|aiohttp|whisper|mediapipe|cv2|opencv|psycopg2|feedparser|bs4|beautifulsoup|lxml|yaml|pyyaml|anthropic|openai|google|googleapiclient|tqdm|slugify|dateutil|matplotlib|seaborn|pydantic'

# Match `import X`, `import X as`, `from X import`, `from X.sub import` at line start.
# Two clauses (POSIX-safe, no \b): (1) denylisted module right after import/from — the trailing
# [^A-Za-z0-9_] also catches the `import yaml;import os` semicolon case; (2) a denylisted module
# later in a comma list (`import os, numpy`).
hits="$(grep -rnE "^[[:space:]]*(import|from)[[:space:]]+(${DENY})([^A-Za-z0-9_]|$)|^[[:space:]]*import[[:space:]].*[ ,](${DENY})([^A-Za-z0-9_]|$)" \
          --include='*.py' scripts/ 2>/dev/null || true)"

if [ -n "$hits" ]; then
  echo "DEPENDENCY-CREEP VIOLATION — third-party import(s) found under scripts/:"
  echo "$hits"
  echo ""
  echo "Only the Python standard library is allowed. Reimplement with stdlib (urllib, json, re, csv, html.parser, ...) or drop the dependency."
  exit 1
fi

# --- Paid Ads red line: a paid SKILL.md must never require a keyed ad-platform API at Tier 1 ---
# Best-effort prose tripwire (heuristic; a sentence mixing "required" with an exonerating word on the
# same line can evade it). The real guarantee is the keyless/own-export framing authored into each skill.
ad_hits="$(grep -rnEi "(google ads|meta( marketing)?|ads platform|marketing) api" --include='SKILL.md' paid/ 2>/dev/null \
  | grep -Ei "require|must have|tier.?1|precondition|necessary" \
  | grep -Eiv "optional|opt-in|tier.?2|tier.?3|mcp|never|not required|own[ -]data|manual export" || true)"
if [ -n "$ad_hits" ]; then
  echo "PAID-ADS RED-LINE VIOLATION — a paid SKILL.md phrases a keyed ad-platform API as required/Tier-1:"
  echo "$ad_hits"
  echo ""
  echo "Paid Ads must score from own-account manual export at Tier 1; keyed ad APIs are opt-in Tier-2/3 MCP only."
  exit 1
fi

echo "moat guard clean — no third-party imports under scripts/, no required keyed ad APIs in paid/."
exit 0
