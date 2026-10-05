#!/bin/bash
# usage: run.sh <script-path> <scenario>
# scenarios: download-fail | install-fail | all-success
SCRIPT="$1"; SCEN="$2"
D="$(cd "$(dirname "$0")" && pwd)"
export PATH="$D/bin:$PATH"
export ZIP_SRC="$D/whl.zip"
rm -rf "$D/run"; mkdir -p "$D/run"; cd "$D/run" || exit 99
case "$SCEN" in
  download-fail) export CURL_MODE=fail ;;
  install-fail)  export CURL_MODE=ok; export RUN_EXIT=1 ;;
  all-success)   export CURL_MODE=ok; export RUN_EXIT=0 ;;
  *) echo "unknown scenario"; exit 98 ;;
esac
echo "### scenario=$SCEN script=$(basename "$SCRIPT")"
bash "$SCRIPT" ascend910b
echo "EXIT_CODE=$?"
