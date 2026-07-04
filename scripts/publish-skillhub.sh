#!/usr/bin/env bash
# publish-skillhub.sh — publish the bundle's skills to skillhub.cn (中文 Skills 社区).
#
# SkillHub is publish-based: each skill goes up with `skillhub publish <dir>`
# under your logged-in account and then enters platform review (pending_review).
# Every SKILL.md already carries the SkillHub frontmatter (slug: aaron-<name>,
# displayName, summary) alongside the Agent Skills fields, so the repo folders
# publish as-is. This script walks the plugin.json skill list so the published
# set always matches the manifest.
#
# Prereqs (one-time):
#   curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
#   skillhub login --key "$SKILLHUB_KEY" --host https://api.skillhub.cn
#   (create the key at skillhub.cn 个人中心 → API keys; real-name verification
#    required before publishing — a 403 means complete it in the browser first)
#
# Usage:
#   bash scripts/publish-skillhub.sh --dry-run                # local pre-check, all 69
#   bash scripts/publish-skillhub.sh --skill keyword-research --dry-run
#   bash scripts/publish-skillhub.sh                          # publish all (changelog 首次发布)
#   bash scripts/publish-skillhub.sh --changelog "v12.7.0 更新说明"
#
# Exit: 0 all requested skills processed, 1 on any failure.

set -u
cd "$(cd "$(dirname "$0")/.." && pwd)"

HOST="https://api.skillhub.cn"
DRY_RUN=0
ONLY_SKILL=""
CHANGELOG="首次发布"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY_RUN=1 ;;
    --skill) shift; ONLY_SKILL="${1:-}" ;;
    --changelog) shift; CHANGELOG="${1:-}" ;;
    --host) shift; HOST="${1:-}" ;;
    *) echo "unknown flag: $1" >&2; exit 1 ;;
  esac
  shift
done

SKILLHUB_BIN="${SKILLHUB_BIN:-$HOME/.local/bin/skillhub}"
command -v skillhub >/dev/null 2>&1 && SKILLHUB_BIN=skillhub
if ! command -v "$SKILLHUB_BIN" >/dev/null 2>&1; then
  echo "FAIL: skillhub CLI not found — install with:" >&2
  echo "  curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only" >&2
  exit 1
fi

SKILL_DIRS=$(python3 -c "
import json
for p in json.load(open('.claude-plugin/plugin.json'))['skills']:
    print(p[2:] if p.startswith('./') else p)
")

fail=0 count=0
for dir in $SKILL_DIRS; do
  name=$(basename "$dir")
  if [ -n "$ONLY_SKILL" ] && [ "$name" != "$ONLY_SKILL" ]; then continue; fi
  if [ ! -f "$dir/SKILL.md" ]; then
    echo "FAIL: $dir/SKILL.md missing" >&2; fail=1; continue
  fi
  slug=$(sed -n 's/^slug: *//p' "$dir/SKILL.md" | head -1)
  if [ -z "$slug" ]; then
    echo "FAIL: no slug in $dir/SKILL.md (SkillHub requires slug/displayName/summary frontmatter)" >&2
    fail=1; continue
  fi

  cmd=("$SKILLHUB_BIN" publish "$dir" --host "$HOST")
  if [ "$DRY_RUN" -eq 1 ]; then
    cmd+=(--dry-run)
    echo "==> $slug (dry-run)"
  else
    cmd+=(--changelog "$CHANGELOG")
    echo "==> $slug"
  fi
  if ! "${cmd[@]}"; then
    echo "FAIL: publish failed for $slug" >&2
    fail=1
  fi
  count=$((count + 1))
done

if [ -n "$ONLY_SKILL" ] && [ "$count" -eq 0 ]; then
  echo "FAIL: skill '$ONLY_SKILL' not found in plugin.json" >&2
  exit 1
fi

suffix=""; [ "$DRY_RUN" -eq 1 ] && suffix=" — dry-run, nothing uploaded"
echo "processed $count skill(s)$suffix"
exit $fail
