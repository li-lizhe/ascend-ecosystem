"""transformers#48937 探针 3：复现 compute_stream 的真实消费点。

关键背景（已从代码确认）：
  input_outputs.py:120-124  <- 本 PR 改动点，让 NPU 上 compute_stream 不再是 None
  model_runner.py:119       <- 消费点（非 CUDA-graph 的 forward 路径）
        maybe_stream = torch.cuda.stream(compute_stream) if compute_stream is not None else nullcontext()

改动前：NPU 上 compute_stream is None -> nullcontext() -> 不炸
改动后：NPU 上 compute_stream 是 NPU stream -> torch.cuda.stream(npu_stream) -> ???

本探针就是把这个 ?? 跑出来。
"""
import inspect
from contextlib import nullcontext

import torch
import torch_npu

dev = torch.device("npu:0")

print("### A. torch.cuda.stream 的实现（解释为什么会炸） ###")
try:
    src = inspect.getsource(torch.cuda.stream)
    for ln in src.splitlines()[:28]:
        print("   ", ln)
except Exception as e:
    print("    取源码失败:", type(e).__name__, e)
print("   torch.cuda._is_compiled() =", torch.cuda._is_compiled())
print("   torch.cuda.is_available() =", torch.cuda.is_available())


def compute_batch_like_model_runner(compute_stream):
    """精确复刻 model_runner.py:119-121 的写法。"""
    maybe_stream = torch.cuda.stream(compute_stream) if compute_stream is not None else nullcontext()
    with maybe_stream:
        return float((torch.ones(4, device=dev) * 2).sum().item())


print("\n### B. 复现 model_runner.py:119 ###")
cases = [
    ("改动前  compute_stream = None                ", None),
    ("改动后  compute_stream = torch.npu.Stream    ", torch.npu.Stream(device=dev)),
    ("评审建议 torch.Stream(device=npu:0)          ", torch.Stream(device=dev)),
]
for label, cs in cases:
    try:
        print("   %s -> OK  sum=%s" % (label, compute_batch_like_model_runner(cs)))
    except Exception as e:
        print("   %s -> ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### C. 候选替代：泛化上下文管理器是否真的切换 current_stream ###")
s = torch.Stream(device=dev)
print("   进入前 torch.npu.current_stream() =", type(torch.npu.current_stream()).__name__)
with s:
    cur = torch.npu.current_stream()
    print("   with torch.Stream(device=npu:0) 内: current_stream =", type(cur).__name__)
    print("   current_stream is s ?", cur is s)
    try:
        print("   torch.accelerator.current_stream() =", type(torch.accelerator.current_stream()).__name__)
    except Exception as e:
        print("   torch.accelerator.current_stream() ERR", type(e).__name__, e)
    print("   该 stream 下跑算子:", float((torch.ones(4, device=dev) * 5).sum().item()))
print("   退出后 torch.npu.current_stream() =", type(torch.npu.current_stream()).__name__)

print("\n### D. torch.accelerator 里的 stream/device 相关 API（找设备无关的替代） ###")
print("   ", sorted(a for a in dir(torch.accelerator) if "stream" in a.lower() or "device" in a.lower()))

print("\n### E. torch.npu.stream(s) 与 s.synchronize() 在两种 stream 上的行为 ###")
for label, st in (("torch.npu.Stream", torch.npu.Stream(device=dev)), ("torch.Stream", torch.Stream(device=dev))):
    try:
        with torch.npu.stream(st):
            r = float((torch.ones(4, device=dev) * 7).sum().item())
        print("   %-16s torch.npu.stream 内跑算子 OK sum=%s ; synchronize -> %s"
              % (label, r, st.synchronize()))
    except Exception as e:
        print("   %-16s ❌ %s: %s" % (label, type(e).__name__, e))
