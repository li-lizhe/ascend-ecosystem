"""transformers#48937 探针 5：判定 `with <stream>:` 到底有没有真正切换当前 stream。

探针 4 用对象身份比较不可靠（torch_npu 的 current_stream() 每次返回新包装对象）。
改用底层 handle（.npu_stream 整数）比较：handle 变了才算真的切过去。
"""
import torch
import torch_npu

dev = torch.device("npu:0")


def h(s):
    return getattr(s, "npu_stream", None)


base = torch.npu.current_stream()
hb = h(base)
print("默认 current_stream: type=%s handle=%s" % (type(base).__qualname__, hb))

s_gen = torch.Stream(device=dev)
s_npu = torch.npu.Stream(device=dev)
print("s_gen  : type=%-30s handle=%s" % (type(s_gen).__qualname__, h(s_gen)))
print("s_npu  : type=%-30s handle=%s" % (type(s_npu).__qualname__, h(s_npu)))

print("\n### with <stream>: 是否切换 ###")
for label, st in (("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        with st:
            c = torch.npu.current_stream()
            print("  with %-22s -> handle=%-16s switched=%s" % (label, h(c), h(c) != hb))
        a = torch.npu.current_stream()
        print("  %-27s 退出后 handle=%-16s 已还原=%s" % ("", h(a), h(a) == hb))
    except Exception as e:
        print("  with %-22s ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 对照：torch.npu.stream(<stream>) ###")
for label, st in (("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        with torch.npu.stream(st):
            c = torch.npu.current_stream()
            print("  torch.npu.stream(%-22s) -> handle=%-16s switched=%s" % (label, h(c), h(c) != hb))
    except Exception as e:
        print("  torch.npu.stream(%-22s) ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 对照：torch.accelerator.set_stream(<stream>) ###")
for label, st in (("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        torch.accelerator.set_stream(st)
        c = torch.npu.current_stream()
        print("  set_stream(%-22s) -> handle=%-16s switched=%s" % (label, h(c), h(c) != hb))
        torch.accelerator.set_stream(base)
    except Exception as e:
        print("  set_stream(%-22s) ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 结论所需：torch.cuda.stream 在无 CUDA 编译的 torch 上会怎样（复述） ###")
from contextlib import nullcontext
for label, st in (("None -> nullcontext", None), ("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        cm = torch.cuda.stream(st) if st is not None else nullcontext()
        with cm:
            r = float((torch.ones(4, device=dev) * 2).sum().item())
        print("  torch.cuda.stream(%-22s) -> OK sum=%s" % (label, r))
    except Exception as e:
        print("  torch.cuda.stream(%-22s) -> ❌ %s: %s" % (label, type(e).__name__, e))
