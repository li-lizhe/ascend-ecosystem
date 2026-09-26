"""transformers#48937 探针 2：泛化 torch.Stream 是否真的满足本 PR 的**实际用法**。

PR 里 compute_stream 的唯一消费点是：
    self.compute_stream.synchronize()          # input_outputs.py:297 / 311
以及 async 路径的 record_event / wait_event（那条路径仍硬编码 torch.cuda.Stream）。

所以「能不能用 torch.Stream 取代 torch.npu.Stream」不能只看构造成功，
必须验证 synchronize / record_event / wait_event / query 这些真实调用。
"""
import traceback
import torch
import torch_npu

dev = torch.device("npu:0")


def t(label, fn):
    try:
        print("  %-52s OK   %s" % (label, fn()))
    except Exception as e:
        print("  %-52s ERR  %s: %s" % (label, type(e).__name__, e))


def ctx_run(cm_factory):
    with cm_factory():
        x = (torch.ones(8, device=dev) * 2).sum().item()
    return "op ran inside, sum=%s" % x


gen = torch.Stream(device=dev)
exp = torch.npu.Stream(device=dev)

print("type(torch.Stream(device=npu:0))     =", type(gen))
print("type(torch.npu.Stream(device=npu:0)) =", type(exp))
print("gen.__mro__ =", [c.__name__ for c in type(gen).__mro__])
print("exp.__mro__ =", [c.__name__ for c in type(exp).__mro__])
print("isinstance(gen, torch.Stream) =", isinstance(gen, torch.Stream),
      "| isinstance(exp, torch.Stream) =", isinstance(exp, torch.Stream))

print("\n=== ① PR 的实际用法：.synchronize() ===")
t("torch.Stream(npu:0).synchronize()", lambda: gen.synchronize())
t("torch.npu.Stream(npu:0).synchronize()", lambda: exp.synchronize())

print("\n=== ② 其它 stream 协议方法 ===")
t("torch.Stream(npu:0).query()", lambda: gen.query())
t("torch.npu.Stream(npu:0).query()", lambda: exp.query())
t("torch.Stream(npu:0).record_event()", lambda: type(gen.record_event()).__name__)
t("torch.npu.Stream(npu:0).record_event()", lambda: type(exp.record_event()).__name__)
ev = torch.Event()
t("torch.Stream(npu:0).wait_event(torch.Event())", lambda: gen.wait_event(ev))
t("torch.npu.Stream(npu:0).wait_event(torch.Event())", lambda: exp.wait_event(ev))

print("\n=== ③ 作为上下文管理器（哪种 API 能包住它） ===")
t("with torch.npu.stream(torch.Stream(npu:0))", lambda: ctx_run(lambda: torch.npu.stream(gen)))
t("with torch.npu.stream(torch.npu.Stream(npu:0))", lambda: ctx_run(lambda: torch.npu.stream(exp)))
t("with torch.Stream(npu:0)  [直接当 ctx]", lambda: ctx_run(lambda: gen))
t("with torch.accelerator.stream(torch.Stream(npu:0))",
  lambda: ctx_run(lambda: torch.accelerator.stream(gen)))
print("\n  注：代码里 _transfer_inputs 用的是 torch.cuda.stream(...)（CUDA 命名空间）")
t("with torch.cuda.stream(torch.Stream(npu:0))", lambda: ctx_run(lambda: torch.cuda.stream(gen)))
t("with torch.cuda.stream(torch.npu.Stream(npu:0))", lambda: ctx_run(lambda: torch.cuda.stream(exp)))

print("\n=== ④ 上下文内 current_stream 是否真的切到 NPU stream ===")
with torch.npu.stream(gen):
    print("   inside torch.npu.stream(gen): torch.npu.current_stream() =", type(torch.npu.current_stream()))
try:
    with torch.accelerator.stream(gen):
        print("   inside torch.accelerator.stream(gen): current =",
              type(torch.accelerator.current_stream()))
except Exception as e:
    print("   accelerator.stream ERR", type(e).__name__, e)

print("\n=== ⑤ CPU 设备上是否也构造得出（评审说 'when not cpu'） ===")
t("torch.Stream(device='cpu')", lambda: type(torch.Stream(device=torch.device('cpu'))).__name__)

print("\n=== ⑥ torch_npu 是否被自动导入（决定 hasattr(torch,'npu') 守卫的意义） ===")
import sys
print("   'torch_npu' in sys.modules =", "torch_npu" in sys.modules)
print("   hasattr(torch, 'npu')      =", hasattr(torch, "npu"))
print("   torch.npu.__file__         =", getattr(torch.npu, "__file__", "?"))
print("   torch.cuda.is_available()  =", torch.cuda.is_available())
