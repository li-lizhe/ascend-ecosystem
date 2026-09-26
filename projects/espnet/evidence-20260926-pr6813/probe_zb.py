\
import os, sys, importlib, types, torch, torch.distributed as dist

MOD     = os.environ["MOD"]                       # batch_master | batch_zero
BACKEND = os.environ.get("BACKEND", "gloo")
DEV     = os.environ.get("DEV", "cpu")            # cpu | npu
COUNTS  = [int(x) for x in os.environ["COUNTS"].split(",")]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
B = importlib.import_module(MOD)                   # 被测文件逐字节原样

# 仅重映射「设备字符串 cuda」与 CUDA 可用性门 —— 使 master 版在无 CUDA 测试机上
# 也能进入分布式分支（在真实 CUDA 机上这两者就是 "cuda" / torch.cuda.is_available()）。
_real_tensor = torch.tensor
def _tensor(data, dtype=None, device=None, **kw):
    if DEV == "npu":
        return _real_tensor(data, dtype=dtype, device="npu:%d" % int(os.environ["RANK"]))
    return _real_tensor(data, dtype=dtype, device="cpu")
B.torch = types.SimpleNamespace(
    tensor=_tensor,
    long=_real_tensor([0]).dtype,          # torch.long：模块里 dtype=torch.long 也走这里
    cuda=types.SimpleNamespace(is_available=lambda: True),
)

if DEV == "npu":
    import torch_npu
    torch.npu.set_device(int(os.environ["RANK"]))

dist.init_process_group(backend=BACKEND)
rank, ws = dist.get_rank(), dist.get_world_size()
assert ws == len(COUNTS), "world_size %d != COUNTS %s" % (ws, COUNTS)

n = COUNTS[rank]
batches = [["b%d" % i] for i in range(n)]
res = err = None
try:
    res = B.synchronize_batches(batches)
except Exception as e:
    err = "%s: %s" % (type(e).__name__, str(e)[:150])

print("[rank%d] backend=%s counts=%s in=%d out=%s err=%s"
      % (rank, dist.get_backend(), COUNTS, n, (len(res) if res is not None else None), err))
dist.barrier()
print("[rank%d] barrier OK (no rank stuck)" % rank)
dist.destroy_process_group()
