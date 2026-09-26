import os, sys, torch, torch.distributed as dist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WHICH = os.environ.get("WHICH", "fixed")
if WHICH == "head":
    from batch_head import synchronize_batches, _current_accelerator_device
elif WHICH == "base":
    from batch_base import synchronize_batches
    _current_accelerator_device = lambda: "N/A (base 无此函数)"
else:
    from batch_fixed import synchronize_batches, _current_accelerator_device

dist.init_process_group(backend="gloo")
rank, ws = dist.get_rank(), dist.get_world_size()
print("[rank%d] WHICH=%s | dist.is_initialized=%s backend=%s ws=%d"
      % (rank, WHICH, dist.is_initialized(), dist.get_backend(), ws))
print("[rank%d] torch.accelerator.is_available()=%s  _current_accelerator_device()=%r"
      % (rank, torch.accelerator.is_available(), _current_accelerator_device()))

n = 5 if rank == 0 else 3
batches = [[i] for i in range(n)]
try:
    out = synchronize_batches(batches)
    if len(out) == n:
        print("[rank%d] in=%d out=%d -> 静默跳过, 未同步 (rank 间不一致!)" % (rank, n, len(out)))
    else:
        print("[rank%d] in=%d out=%d -> 已同步" % (rank, n, len(out)))
except Exception as e:
    print("[rank%d] in=%d -> 显式报错 %s: %s" % (rank, n, type(e).__name__, str(e)[:110]))
dist.barrier()
print("[rank%d] barrier 通过 -> 没有 rank 卡在集合通信上" % rank)
dist.destroy_process_group()
