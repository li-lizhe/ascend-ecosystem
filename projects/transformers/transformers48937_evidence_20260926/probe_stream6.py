"""transformers#48937 探针 6：验证「设备无关 stream 上下文」helper 的确切实现。

helper 必须：
  * compute_stream is None      -> nullcontext()（与现状一致）
  * CUDA stream                 -> torch.cuda.stream(s)（保持原行为，CUDA 上不可在本机验证，故不动）
  * NPU / XPU / 泛化 torch.Stream -> 直接用 stream 自身当上下文管理器
"""
import inspect
from contextlib import nullcontext

import torch
import torch_npu

print("### torch.cuda.StreamContext 源码（解释为何泛化 torch.Stream 不能喂给 torch.cuda.stream）###")
try:
    for ln in inspect.getsource(torch.cuda.StreamContext).splitlines()[:22]:
        print("   ", ln)
except Exception as e:
    print("    取源码失败:", type(e).__name__, e)


def stream_context(stream):
    """Run enclosed ops on `stream`, whichever accelerator it was created on."""
    if stream is None:
        return nullcontext()
    if stream.device.type == "cuda":
        return torch.cuda.stream(stream)
    return stream


dev = torch.device("npu:0")


def h(s):
    return getattr(s, "npu_stream", None)


base = torch.npu.current_stream()
hb = h(base)

print("\n### 验证 helper ###")
cases = [
    ("None                 -> nullcontext", None),
    ("torch.Stream(npu:0)  -> 自身当 ctx  ", torch.Stream(device=dev)),
    ("torch.npu.Stream(npu:0) -> 自身当 ctx", torch.npu.Stream(device=dev)),
]
for label, st in cases:
    try:
        with stream_context(st):
            cur = torch.npu.current_stream()
            r = float((torch.ones(16, device=dev) * 2).sum().item())
            switched = (h(cur) != hb) if st is not None else (h(cur) == hb)
        restored = h(torch.npu.current_stream()) == hb
        print("   %s -> OK sum=%-6s switched=%-5s restored=%s" % (label, r, switched, restored))
    except Exception as e:
        print("   %s -> ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 关键：泛化 torch.Stream 缺 .cuda_stream（说明为何 CUDA 分支必须保留）###")
gs = torch.Stream(device=dev)
print("   torch.Stream(device=npu:0).cuda_stream 存在? ", hasattr(gs, "cuda_stream"))
print("   torch.cuda.Stream 是否继承 torch.Stream ?  ",
      issubclass(torch.cuda.Stream, torch.Stream))
print("   torch.npu.Stream 是否继承 torch.Stream ?   ",
      issubclass(torch.npu.Stream, torch.Stream))
