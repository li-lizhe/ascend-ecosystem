"""transformers#48937 验证：NPU 上 `torch.Stream(device=...)` 能否替代显式 `torch.npu.Stream`。

背景
  PR 当前写法（3 分支）：
      self.compute_stream = torch.cuda.Stream(device=self.device) if device.type == "cuda" else None
      if hasattr(torch, "npu") and device.type == "npu":
          self.compute_stream = torch.npu.Stream(device=self.device)
      elif hasattr(torch, "xpu") and device.type == "xpu":
          self.compute_stream = torch.Stream(device=self.device)

  评审 IlyasMoutawwakil 行内问：「can't we use torch.Stream always when not cpu ?」
  我们回复里承诺：先在昇腾真机上确认 `torch.Stream` 的 NPU dispatch 是否成立，再回来 follow up。

本探针要回答
  Q1 `torch.Stream(device=npu:0)` 能否构造？构造出的是什么类？
  Q2 它与 `torch.npu.Stream(device=npu:0)` 是否等价（同一类 / 同 device / 能否互换使用）？
  Q3 它能否当上下文管理器用（真实跑一个 NPU 算子），即是否**功能可用**而非只是构造成功？
  Q4 `torch.Stream` 的 NPU 分派是靠什么成立的（torch_npu 是否注册了 stream 实现）？
"""
import inspect
import sys
import traceback

print("=" * 78)
print("Python", sys.version.split()[0])
import torch
print("torch", torch.__version__)
print("torch.__file__", torch.__file__)
try:
    import torch_npu
    print("torch_npu", getattr(torch_npu, "__version__", "?"))
except Exception as e:
    print("❌ torch_npu 导入失败:", type(e).__name__, e)
    sys.exit(2)

print("torch.npu.is_available() =", torch.npu.is_available(),
      "| device_count =", torch.npu.device_count())
try:
    print("torch.accelerator.current_accelerator() =", torch.accelerator.current_accelerator())
except Exception as e:
    print("accelerator ERR", e)

print("\n--- Q4 torch.Stream 实现（决定分派方式）---")
try:
    src = inspect.getsource(torch.Stream)
    print(src[:1400])
except Exception as e:
    print("取源码失败:", type(e).__name__, e)
    print("torch.Stream =", torch.Stream, "| module:", getattr(torch.Stream, "__module__", "?"),
          "| qualname:", getattr(torch.Stream, "__qualname__", "?"))

dev = torch.device("npu:0")
print("\n--- Q1/Q2/Q3 实测 (device=%s) ---" % dev)

print("\n[A] 显式 torch.npu.Stream")
try:
    a = torch.npu.Stream(device=dev)
    print("    OK  type=%s  device=%s  npu_stream=%s"
          % (type(a), getattr(a, "device", "?"), getattr(a, "npu_stream", "?")))
except Exception as e:
    print("    ERR %s: %s" % (type(e).__name__, e)); a = None

print("\n[B] 泛化 torch.Stream（评审建议的写法）")
try:
    b = torch.Stream(device=dev)
    print("    OK  type=%s  device=%s  npu_stream=%s"
          % (type(b), getattr(b, "device", "?"), getattr(b, "npu_stream", "?")))
except Exception as e:
    print("    ERR %s: %s" % (type(e).__name__, e)); b = None
    traceback.print_exc()

print("\n[C] 泛化 torch.Stream 作为上下文管理器 + 真实 NPU 算子")
try:
    with torch.Stream(device=dev) as s:
        t = torch.ones(8, device=dev)
        r = float((t * 3).sum().item())
        cur_inside = torch.npu.current_stream()
    print("    OK  sum=%s  上下文内 current_stream=%s" % (r, type(cur_inside)))
except Exception as e:
    print("    ERR %s: %s" % (type(e).__name__, e)); traceback.print_exc()

print("\n[D] 等价性判定")
try:
    print("    torch.Stream is torch.npu.Stream      ->", torch.Stream is torch.npu.Stream)
except Exception as e:
    print("    ERR", e)
if a is not None and b is not None:
    print("    type(A) == type(B)                    ->", type(a) == type(b))
    print("    A.device == B.device                  ->", getattr(a, "device", None) == getattr(b, "device", None))
    try:
        print("    B 能用于 torch.npu.stream(B)          ->", end=" ")
        with torch.npu.stream(b):
            _ = (torch.ones(4, device=dev) * 2).sum().item()
        print("OK")
    except Exception as e:
        print("ERR %s: %s" % (type(e).__name__, e))
    try:
        print("    A 能用于 torch.npu.stream(A)          ->", end=" ")
        with torch.npu.stream(a):
            _ = (torch.ones(4, device=dev) * 2).sum().item()
        print("OK")
    except Exception as e:
        print("ERR %s: %s" % (type(e).__name__, e))

print("\n[E] 评审建议的收敛写法是否真的能跑（`device.type != 'cpu'` 分支）")
try:
    _d = torch.device("npu:0")
    compute_stream = torch.Stream(device=_d) if _d.type != "cpu" else None
    print("    compute_stream =", type(compute_stream), getattr(compute_stream, "device", None))
    with torch.npu.stream(compute_stream):
        out = (torch.ones(16, device=_d) + 1).sum().item()
    print("    在该 stream 下跑算子 OK, sum =", out)
except Exception as e:
    print("    ERR %s: %s" % (type(e).__name__, e)); traceback.print_exc()

print("\n[F] 反例对照：不 import torch_npu 时 torch.Stream(device='npu:0') 会怎样")
print("    （无法在本进程内测，需另起进程；见 run 脚本的 no_torch_npu 分支）")
print("=" * 78)
