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
hits="$(grep -rnE "^[[:space:]]*(import|from)[[:space:]]+(${DENY})([[:space:].]|[[:space:]]+import|$)" \
          --include='*.py' scripts/ 2>/dev/null || true)"

if [ -n "$hits" ]; then
  echo "DEPENDENCY-CREEP VIOLATION — third-party import(s) found under scripts/:"
  echo "$hits"
  echo ""
  echo "Only the Python standard library is allowed. Reimplement with stdlib (urllib, json, re, csv, html.parser, ...) or drop the dependency."
  exit 1
fi

echo "stdlib-only check clean — no third-party imports under scripts/."
exit 0
