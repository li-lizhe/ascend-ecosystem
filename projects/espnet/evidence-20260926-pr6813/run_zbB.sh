#!/bin/bash
PY=/opt/miniconda/envs/npu215/bin/python
cd /workspace/espnet6808 || exit 1
source /opt/ascend/cann-9.2.0-beta.2/set_env.sh
export LD_LIBRARY_PATH=/opt/miniconda/envs/npu215/lib:$LD_LIBRARY_PATH
echo "############ B. HCCL（真加速器 910B2）before/after ############"
for counts in 5,0 5,2 5,3; do
  for mod in batch_master batch_zero; do
    echo "--- counts=$counts  mod=$mod"
    MOD=$mod COUNTS=$counts BACKEND=hccl DEV=npu timeout 300 \
      $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_zb.py 2>&1 \
      | grep -E "^\[rank[01]\]|RuntimeError|AssertionError|Traceback" | head -6
  done
done
