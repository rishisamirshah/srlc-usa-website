#!/bin/bash
# Daily (launchd: com.rishi.srlc-stats): rebuild with the figures on
# loveandcare.srmd.org and deploy if any changed. Skips when the working tree
# has uncommitted work, so it never sweeps a half-done edit into a commit.
set -euo pipefail
cd "$(dirname "$0")/.."
echo "== $(date '+%Y-%m-%d %H:%M:%S')"
if [ -n "$(git status --porcelain)" ]; then echo "working tree has uncommitted changes, skipping"; exit 0; fi
git pull --ff-only -q
python3 gen/build.py > /dev/null
if git diff --quiet -- gen/stats_live.json; then
  git checkout -q -- . && git clean -qfd -- assets/css assets/js
  echo "figures unchanged"; exit 0
fi
git add -A
git commit -q -m "Stats from loveandcare.srmd.org" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git push -q origin main
netlify deploy --prod --dir . --site 51fd272d-74e6-429e-9c66-31fbc724335a | grep -E "Deploy is live|Error" || true
echo "deployed: $(tr -d '\n ' < gen/stats_live.json)"
