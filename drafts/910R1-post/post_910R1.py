#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""发布 #2529/#2530/#2531 的中文回帖到 triton-lang/triton-ascend（GitHub）。

用法：
    python post_910R1.py            # dry-run：只打印将发布的正文与目标，不发送
    python post_910R1.py --go       # 真发，并在发完后回读 API 逐字校验
    python post_910R1.py --verify   # 只做回读校验（不发送）

正文来源：drafts/910R1-post/body_<n>.md（由 build_bodies.py 生成，逐字发布）。
"""
import json
import os
import subprocess
import sys

REPO = "triton-lang/triton-ascend"
HERE = os.path.dirname(os.path.abspath(__file__))
POSTDIR = HERE  # 脚本与正文同目录
TOKEN_FILE = r"C:\Users\华为\.config\ghtoken"
PROXY = "socks5h://127.0.0.1:10808"
NUMBERS = [2529, 2530, 2531]


def token():
    with open(TOKEN_FILE, encoding="utf-8") as fh:
        return fh.read().strip()


def http(url, *, method="GET", data=None, timeout=25):
    """Direct first, SOCKS fallback. Returns (http_code, body_text)."""
    tok = token()
    hdrs = ["-H", "Authorization: token " + tok,
            "-H", "Accept: application/vnd.github+json",
            "-H", "User-Agent: hermes-post-910R1",
            "-H", "X-GitHub-Api-Version: 2022-11-28"]
    for px in (None, PROXY):
        args = ["curl", "-s", "-w", "%{http_code}", "--max-time", str(timeout),
                "--connect-timeout", "10"]
        if px:
            args += ["-x", px]
        args += ["-X", method] + hdrs
        if data is not None:
            args += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        args += [url]
        r = subprocess.run(args, input=data, capture_output=True, text=True,
                           encoding="utf-8", timeout=timeout + 10)
        out = r.stdout or ""
        code, _, body = out.rpartition("}")[0], "", ""
        # curl appends the http code at the very end; split it off
        if len(out) >= 3 and out[-3:].isdigit():
            code, body = out[-3:], out[:-3]
        else:
            code, body = "000", out
        if code != "000":
            return code, body
    return "000", ""


def body_path(n):
    return os.path.join(POSTDIR, f"body_{n}.md")


def do_post(n):
    text = open(body_path(n), encoding="utf-8").read()
    payload = json.dumps({"body": text}, ensure_ascii=False)
    url = f"https://api.github.com/repos/{REPO}/issues/{n}/comments"
    code, body = http(url, method="POST", data=payload, timeout=40)
    print(f"#{n} POST -> HTTP {code}")
    if code != "201":
        print("   FAILED body:", body[:500])
        return None
    d = json.loads(body)
    print(f"   comment id={d['id']} url={d['html_url']}")
    return d


def verify(n):
    url = f"https://api.github.com/repos/{REPO}/issues/{n}/comments?per_page=100"
    code, body = http(url)
    if code != "200":
        print(f"#{n} verify FAILED HTTP {code}: {body[:200]}")
        return False
    local = open(body_path(n), encoding="utf-8").read()
    mine = [c for c in json.loads(body) if c["user"]["login"] == "li-lizhe"]
    if not mine:
        print(f"#{n} 回读：未找到我方评论")
        return False
    last = mine[-1]
    remote = last["body"]
    ok = remote.strip() == local.strip()
    print(f"#{n} 回读 id={last['id']} 本地 {len(local)} chars / 远端 {len(remote)} chars "
          f"/ 逐字一致={ok} / url={last['html_url']}")
    return ok


def main():
    go = "--go" in sys.argv
    only_verify = "--verify" in sys.argv
    if only_verify:
        for n in NUMBERS:
            verify(n)
        return
    for n in NUMBERS:
        text = open(body_path(n), encoding="utf-8").read()
        print("=" * 70)
        print(f"#{n} 正文 {len(text)} chars, 前 120 字: {text[:120]!r}")
        if not go:
            continue
        do_post(n)
    if not go:
        print("\n（dry-run 结束，未发送。加 --go 真发）")
        return
    print("\n=== 回读校验 ===")
    allok = True
    for n in NUMBERS:
        allok &= verify(n)
    print("ALL_OK" if allok else "SOME_FAILED")


if __name__ == "__main__":
    main()
