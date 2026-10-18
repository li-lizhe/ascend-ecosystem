#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""创建 PR: triton-lang/triton-ascend <-- li-lizhe:fix/2530-useindexinput

  python open_pr_2530.py            # dry-run
  python open_pr_2530.py --go       # 真开
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = open(os.path.expandvars(r"C:\Users\华为\.config\ghtoken"), encoding="utf-8").read().strip()
API = "https://api.github.com/repos/triton-lang/triton-ascend"
BODY = open(os.path.join(HERE, "pr_body_2530.md"), encoding="utf-8").read()

PAYLOAD = {
    "title": "fix(TritonToLinalg): annotate the index input of max/min-with-index reductions",
    "head": "li-lizhe:fix/2530-useindexinput",
    "base": "main",
    "body": BODY,
    "draft": False,
}


def main():
    if "--go" not in sys.argv:
        print("=== DRY RUN ===")
        for k, v in PAYLOAD.items():
            if k == "body":
                print(f"{k}: ({len(v)} chars)")
            else:
                print(f"{k}: {v}")
        print("\n--- body ---")
        print(BODY)
        return

    tmp = os.path.join(HERE, "_pr.json")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(PAYLOAD, f, ensure_ascii=False)
    r = subprocess.run([
        "curl", "-s", "--max-time", "90", "-X", "POST", API + "/pulls",
        "-H", "Authorization: token " + TOK,
        "-H", "Accept: application/vnd.github+json",
        "-H", "User-Agent: hermes-ghnet",
        "-H", "Content-Type: application/json",
        "--data-binary", "@" + tmp,
    ], capture_output=True, text=True, timeout=120)
    try:
        os.remove(tmp)
    except OSError:
        pass
    try:
        j = json.loads(r.stdout)
    except Exception:
        print("非 json 响应:", r.stdout[:500]); return
    if "number" in j:
        print("PR 已创建: #%s" % j["number"])
        print("url:", j["html_url"])
    else:
        print("失败:", json.dumps(j, ensure_ascii=False)[:600])


main()
