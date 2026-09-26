import os, sys, torch
print("TORCH_DEVICE_BACKEND_AUTOLOAD =", os.environ.get("TORCH_DEVICE_BACKEND_AUTOLOAD"))
print("ASCEND_HOME_PATH            =", os.environ.get("ASCEND_HOME_PATH"))
print("LD_LIBRARY_PATH 含 hccl 目录 =", any("hccl" in p or "Ascend" in p for p in os.environ.get("LD_LIBRARY_PATH","").split(":")))
print("只 import torch 后, 'torch_npu' in sys.modules =", "torch_npu" in sys.modules)
print("torch.accelerator.is_available() =", torch.accelerator.is_available())
print("current_accelerator() =", torch.accelerator.current_accelerator())
print("_get_privateuse1_backend_name() =", torch._C._get_privateuse1_backend_name())
