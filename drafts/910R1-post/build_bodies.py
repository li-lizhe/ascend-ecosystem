#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""组装 #2529/#2530/#2531 的最终回帖正文（模板 + 自包含脚本内联）。

输入：drafts/910R1-post/tpl_<n>.md（含 <<<SCRIPT>>> 占位）
      D:/ascend/work/issue5376/evidence_910/{repro_2531.py,repro_2530.py,probe_2529.py}
输出：drafts/910R1-post/body_<n>.md  ← 逐字发布用
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
POST = HERE  # 脚本与模板同目录
EV = r"D:\ascend\work\issue5376\evidence_910"

JOBS = [
    (2531, "repro_2531.py"),
    (2530, "repro_2530.py"),
    (2529, "probe_2529.py"),
]

for num, script in JOBS:
    tpl = open(os.path.join(POST, f"tpl_{num}.md"), encoding="utf-8").read()
    src = open(os.path.join(EV, script), encoding="utf-8").read().rstrip("\n")
    assert tpl.count("<<<SCRIPT>>>") == 1, (num, tpl.count("<<<SCRIPT>>>"))
    body = tpl.replace("<<<SCRIPT>>>", src)
    out = os.path.join(POST, f"body_{num}.md")
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print(f"#{num}: tpl={len(tpl)} src={len(src)} body={len(body)} -> {out}")
    assert "<<<SCRIPT>>>" not in body
    # sanity: 中文仍在，脚本头在
    assert f"issue #{num}" in body, num
print("OK")
