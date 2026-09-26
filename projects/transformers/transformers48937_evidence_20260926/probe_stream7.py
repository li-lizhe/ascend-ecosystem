"""transformers#48937 探针 7：`device.type != "cpu"` 这个泛化条件是否会把非加速器设备也吞进来。

原写法只在 cuda/npu/xpu 三种 device.type 下建 stream，其它（如 mps）保持 None。
若改成 `elif device.type != "cpu"`，需要确认 mps/meta 等不会因为构造 torch.Stream 而抛错。
"""
import torch
import torch_npu

print("torch", torch.__version__, "| torch_npu", torch_npu.__version__)
print()
for dt in ("cpu", "cuda", "npu", "xpu", "mps", "meta", "privateuseone"):
    try:
        d = torch.device(dt)
    except Exception as e:
        print("  %-14s torch.device() 本身就失败: %s: %s" % (dt, type(e).__name__, e))
        continue
    try:
        s = torch.Stream(device=d)
        print("  %-14s torch.Stream(device=%s) -> OK  type=%s device=%s"
              % (dt, d, type(s).__module__ + "." + type(s).__qualname__, getattr(s, "device", None)))
    except Exception as e:
        print("  %-14s torch.Stream(device=%s) -> ❌ %s: %s" % (dt, d, type(e).__name__, e))
    try:
        print("  %-14s   .device.type 可读 -> %r" % (dt, torch.Stream(device=d).device.type))
    except Exception:
        pass
print()
print("参考：accelerator 报告的当前加速器 =", torch.accelerator.current_accelerator())
