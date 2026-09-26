import torch
def st(tag):
    A = torch.accelerator
    print("[%s] torch=%s" % (tag, torch.__version__))
    print("   accelerator.is_available() = %s" % A.is_available())
    print("   accelerator.current_accelerator() = %r" % A.current_accelerator())
    try:
        print("   accelerator.device_count() = %s" % A.device_count())
    except Exception as e:
        print("   accelerator.device_count() -> %s: %s" % (type(e).__name__, e))
    print("   torch.cuda.is_available() = %s" % torch.cuda.is_available())
st("只 import torch")
import torch_npu
st("import torch_npu 之后")
print("torch_npu 版本:", torch_npu.__version__)
print("PrivateUse1 后端名:", torch._C._get_privateuse1_backend_name())
print("get_default_backend_for_device('npu'):", torch.distributed.get_default_backend_for_device("npu"))
