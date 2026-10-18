#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""发 #2529 结论评论并关闭 issue。

  python post_close_2529.py            # dry-run，打印将发送的正文
  python post_close_2529.py --verify   # 检查当前是否已有关闭评论
  python post_close_2529.py --go       # 真发：评论 + close
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = open(os.path.expandvars(r"C:\Users\华为\.config\ghtoken"), encoding="utf-8").read().strip()
API = "https://api.github.com/repos/triton-lang/triton-ascend"
ISSUE = 2529


def curl(args, timeout=60):
    r = subprocess.run(["curl", "-s", "--max-time", str(timeout)] + args,
                       capture_output=True, text=True, timeout=timeout + 10)
    return r.stdout


def post_json(url, payload):
    """经 stdin 传 json，避免命令行中文/长度问题。"""
    body = json.dumps(payload, ensure_ascii=False)
    tmp = os.path.join(HERE, "_payload.json")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(body)
    try:
        return curl([
            "-X", "POST", url,
            "-H", "Authorization: token " + TOK,
            "-H", "Accept: application/vnd.github+json",
            "-H", "User-Agent: hermes-ghnet",
            "-H", "Content-Type: application/json",
            "--data-binary", "@" + tmp,
        ])
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def main():
    body = open(os.path.join(HERE, "body_2529_final.md"), encoding="utf-8").read()

    if "--verify" in sys.argv:
        c = json.loads(curl(["-H", "Authorization: token " + TOK, API + f"/issues/{ISSUE}"]))
        cs = json.loads(curl(["-H", "Authorization: token " + TOK, API + f"/issues/{ISSUE}/comments?per_page=100"]))
        print("issue state:", c.get("state"), "| comments:", len(cs))
        for x in cs:
            print("  -", x["user"]["login"], x["created_at"][:16], (x["body"] or "")[:60].replace("\n", " "))
        return

    if "--go" not in sys.argv:
        print("=== DRY RUN 正文 (%d 字符) ===" % len(body))
        print(body)
        print("=== 待执行：POST /issues/%d/comments  +  PATCH state=closed ===" % ISSUE)
        return

    r1 = post_json(API + f"/issues/{ISSUE}/comments", {"body": body})
    try:
        j1 = json.loads(r1)
    except Exception:
        print("POST comment 响应非 json:", r1[:300]); return
    if "id" not in j1:
        print("POST comment 失败:", r1[:400]); return
    print("评论已发: id=%s  url=%s" % (j1["id"], j1.get("html_url")))

    r2 = post_json(API + f"/issues/{ISSUE}", {"state": "closed", "state_reason": "not_planned"})
    try:
        j2 = json.loads(r2)
    except Exception:
        print("PATCH 响应非 json:", r2[:300]); return
    print("issue 状态: %s (reason=%s)" % (j2.get("state"), j2.get("state_reason")))


main()
