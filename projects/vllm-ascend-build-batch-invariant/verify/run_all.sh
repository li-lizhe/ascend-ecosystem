#!/bin/bash
cd "$(dirname "$0")" || exit 1
D="$(pwd)"
PY="$D/bin/python"
"$PY" mkzip.py
for s in download-fail install-fail all-success; do
  for v in before after; do
    bash run.sh "$D/$v.sh" "$s" 2>&1 | grep -v "parallel jobs"
    echo
  done
done
