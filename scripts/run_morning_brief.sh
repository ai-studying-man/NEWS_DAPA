#!/usr/bin/env sh
set -eu

repo_root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$repo_root"
mkdir -p logs

if command -v uv >/dev/null 2>&1; then
  uv run dapa-morning-brief --days 3 --fallback-days 5 >> logs/dapa_morning_brief.log 2>&1
else
  PYTHONPATH="$repo_root/src" python -m dapa_morning_brief.cli --days 3 --fallback-days 5 >> logs/dapa_morning_brief.log 2>&1
fi
