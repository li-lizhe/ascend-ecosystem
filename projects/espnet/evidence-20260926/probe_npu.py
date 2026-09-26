import os, sys, torch, torch_npu, torch.distributed as dist
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
WHICH = os.environ.get("WHICH", "fixed")
if WHICH == "base":
    from batch_base import synchronize_batches
    _cad = lambda: "N/A"
else:
    from batch_fixed import synchronize_batches, _current_accelerator_device as _cad

rank = int(os.environ.get("RANK", "0"))
torch.npu.set_device(rank)
dist.init_process_group(backend="hccl")
print("[rank%d] WHICH=%s dist=%s backend=%s accelerator=%s device=%r"
      % (rank, WHICH, dist.is_initialized(), dist.get_backend(),
         torch.accelerator.is_available(), _cad()))
n = 5 if rank == 0 else 3
out = synchronize_batches([[i] for i in range(n)])
print("[rank%d] in=%d out=%d expected_out=5  -> %s"
      % (rank, n, len(out), "OK 已同步" if len(out) == 5 else "FAIL 未同步"))
dist.barrier()
print("[rank%d] HCCL barrier OK" % rank)
dist.destroy_process_group()
