#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""逐字回读校验 #2529 发布评论与本地文件是否一致。"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
TOK = open(os.path.expandvars(r"C:\Users\华为\.config\ghtoken"), encoding="utf-8").read().strip()
API = "https://api.github.com/repos/triton-lang/triton-ascend"

out = subprocess.run(["curl", "-s", "--max-time", "60",
                      "-H", "Authorization: token " + TOK,
                      API + "/issues/2529/comments?per_page=100"],
                     capture_output=True, text=True).stdout
cs = json.loads(out)
mine = [c for c in cs if c["user"]["login"] == "li-lizhe"][-1]
remote = mine["body"].replace("\r\n", "\n").strip()
local = open(os.path.join(HERE, "body_2529_final.md"), encoding="utf-8").read().replace("\r\n", "\n").strip()

print("远端 id:", mine["id"], "| 长度:", len(remote), "| 本地长度:", len(local))
print("逐字一致:", remote == local)
if remote != local:
    import difflib
    for l in list(difflib.unified_diff(local.split("\n"), remote.split("\n"), "local", "remote", lineterm=""))[:40]:
        print(l)
