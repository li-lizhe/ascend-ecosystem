"""transformers#48937 探针 4：确定「设备无关的 stream 上下文」正确写法。

消费点 model_runner.py:119 等目前写的是 torch.cuda.stream(compute_stream)，
在无 CUDA 编译的 torch 上会 AssertionError。要找的是能同时覆盖 cuda/npu/xpu 的写法。
"""
import torch
import torch_npu

dev = torch.device("npu:0")


def ft(x):
    return "%s.%s" % (type(x).__module__, type(x).__qualname__)


s_gen = torch.Stream(device=dev)
s_npu = torch.npu.Stream(device=dev)

print("s_gen =", ft(s_gen))
print("s_npu =", ft(s_npu))
print("isinstance(s_npu, torch.Stream) =", isinstance(s_npu, torch.Stream))
print("torch.cuda.Stream.__mro__ =", [c.__name__ for c in torch.cuda.Stream.__mro__])
print("torch.Stream.__mro__     =", [c.__name__ for c in torch.Stream.__mro__])

print("\n### 1. `with <stream>:` 是否真的把 current_stream 切过去 ###")
print("before:", ft(torch.accelerator.current_stream()))
for label, st in (("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        with st:
            c = torch.accelerator.current_stream()
            n = torch.npu.current_stream()
            print("  with %-24s -> accelerator.current_stream()=%s (is it? %s) | npu.current_stream()=%s (is it? %s)"
                  % (label, ft(c), c is st, ft(n), n is st))
    except Exception as e:
        print("  with %-24s ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 2. torch.accelerator.set_stream / current_stream（设备无关 API）###")
for label, st in (("torch.Stream(npu:0)", s_gen), ("torch.npu.Stream(npu:0)", s_npu)):
    try:
        prev = torch.accelerator.current_stream()
        torch.accelerator.set_stream(st)
        now = torch.accelerator.current_stream()
        torch.accelerator.set_stream(prev)
        print("  set_stream(%-24s) -> current_stream()=%s (is it? %s)" % (label, ft(now), now is st))
    except Exception as e:
        print("  set_stream(%-24s) ❌ %s: %s" % (label, type(e).__name__, e))

print("\n### 3. 设备无关上下文管理器的候选实现，逐个验证 ###")
from contextlib import contextmanager, nullcontext


@contextmanager
def stream_ctx_accel(s):
    """候选 A：用 torch.accelerator.set_stream 切换/还原。"""
    if s is None:
        yield
        return
    prev = torch.accelerator.current_stream()
    torch.accelerator.set_stream(s)
    try:
        yield
    finally:
        torch.accelerator.set_stream(prev)


@contextmanager
def stream_ctx_enter(s):
    """候选 B：直接用 stream 自身的 __enter__/__exit__。"""
    if s is None:
        yield
        return
    with s:
        yield


def probe_ctx(name, cm_factory, st):
    try:
        with cm_factory(st):
            inside = torch.accelerator.current_stream()
            val = float((torch.ones(8, device=dev) * 3).sum().item())
        after = torch.accelerator.current_stream()
        ok = inside is st
        print("  %-46s OK  sum=%-6s 内部current_is_stream=%s  退出已还原=%s"
              % (name, val, ok, after is not st or st is None))
    except Exception as e:
        print("  %-46s ❌ %s: %s" % (name, type(e).__name__, e))


probe_ctx("A accelerator.set_stream + torch.Stream(npu)", stream_ctx_accel, s_gen)
probe_ctx("A accelerator.set_stream + torch.npu.Stream  ", stream_ctx_accel, s_npu)
probe_ctx("B `with s:` + torch.Stream(npu)             ", stream_ctx_enter, s_gen)
probe_ctx("B `with s:` + torch.npu.Stream              ", stream_ctx_enter, s_npu)
probe_ctx("nullcontext (compute_stream is None)        ", lambda s: nullcontext(), None)

print("\n### 4. 事件序是否真的生效（在 s 上排队 -> 同步）###")
try:
    s = torch.Stream(device=dev)
    with torch.npu.stream(s):
        t = torch.ones(1024, device=dev)
        r = t.sum()
    s.synchronize()
    print("  npu.stream(s) 内跑 1024 求和 -> %s ; s.synchronize() OK" % r.item())
except Exception as e:
    print("  ❌", type(e).__name__, e)
