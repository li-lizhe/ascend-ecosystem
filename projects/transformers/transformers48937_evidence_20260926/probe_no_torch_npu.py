"""对照：不 import torch_npu 时，泛化 torch.Stream(device='npu:0') 的行为。

用来回答「torch.Stream 的 NPU 分派是否依赖 torch_npu 被导入/注册」。
"""
import torch
print("torch", torch.__version__)
print("hasattr(torch, 'npu')            =", hasattr(torch, "npu"))
try:
    print("torch.accelerator.current_accelerator() =", torch.accelerator.current_accelerator())
except Exception as e:
    print("accelerator ERR", type(e).__name__, e)
try:
    d = torch.device("npu:0")
    print("torch.device('npu:0')           ->", d, "| .type =", d.type)
except Exception as e:
    print("torch.device ERR", type(e).__name__, e)
    d = None
try:
    s = torch.Stream(device=torch.device("npu:0"))
    print("torch.Stream(device=npu:0)      ->", type(s), "| device =", getattr(s, "device", None))
except Exception as e:
    print("torch.Stream(device=npu:0) ERR  ->", type(e).__name__, e)
try:
    s = torch.Stream(device="npu:0")
    print("torch.Stream(device='npu:0')    ->", type(s), "| device =", getattr(s, "device", None))
except Exception as e:
    print("torch.Stream(device='npu:0') ERR->", type(e).__name__, e)
