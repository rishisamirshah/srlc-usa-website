#!/bin/bash
# Face data for every site photo (Naman, Oct 22: no face cut off anywhere).
# Compiles faces.swift (macOS Vision) and writes faces.jsonl, which audit.mjs
# and fit.py read. Rerun after adding or replacing photos.
#   gen/qa/faces.sh
#   node gen/qa/audit.mjs http://localhost:8790 1920,1440,1024,390 /about/who-we-are/
set -e
QA="$(cd "$(dirname "$0")" && pwd)"; ROOT="$QA/../.."
mkdir -p "$QA/.bin"
[ "$QA/.bin/faces" -nt "$QA/faces.swift" ] || swiftc -O "$QA/faces.swift" -o "$QA/.bin/faces"
cd "$ROOT"
find assets/img -type f \( -name '*.webp' -o -name '*.jpg' -o -name '*.jpeg' -o -name '*.png' \) -not -path '*/logo/*' -not -path '*/badges/*' -print0 \
  | xargs -0 -n 10 -P 8 "$QA/.bin/faces" | sort > "$QA/faces.jsonl"
wc -l < "$QA/faces.jsonl"
