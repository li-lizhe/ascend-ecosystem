#!/bin/bash
# espnet#6808 姊妹 PR（零 batch + 补齐）真机验证
PY=/opt/miniconda/envs/npu215/bin/python
cd /workspace/espnet6808 || exit 1
echo "=== 被测文件 md5 ==="
md5sum batch_master.py batch_zero.py test_batch_zero.py

echo
echo "############ A. gloo（CPU，无需 accelerator）before/after 对照 ############"
for counts in 5,0 5,2 5,3 0,0; do
  for mod in batch_master batch_zero; do
    echo "--- counts=$counts  mod=$mod"
    MOD=$mod COUNTS=$counts BACKEND=gloo DEV=cpu timeout 180 \
      $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_zb.py 2>&1 \
      | grep -E "^\[rank[01]\]|RuntimeError|AssertionError|Traceback" | head -6
  done
done

echo
echo "############ B. HCCL（真加速器 910B2）before/after ############"
source /opt/ascend/cann-9.2.0-beta.2/set_env.sh >/dev/null 2>&1
export LD_LIBRARY_PATH=/opt/miniconda/envs/npu215/lib:$LD_LIBRARY_PATH
for counts in 5,0 5,2 5,3; do
  for mod in batch_master batch_zero; do
    echo "--- counts=$counts  mod=$mod"
    MOD=$mod COUNTS=$counts BACKEND=hccl DEV=npu timeout 300 \
      $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_zb.py 2>&1 \
      | grep -E "^\[rank[01]\]|RuntimeError|AssertionError|Traceback|Error" | head -6
  done
done

echo
echo "############ C. 上游单测（原文 + 新增 3 例），最小包壳 ############"
rm -rf shim && mkdir -p shim/espnet2/speechlm/dataloader
touch shim/espnet2/__init__.py shim/espnet2/speechlm/__init__.py shim/espnet2/speechlm/dataloader/__init__.py
cp batch_zero.py shim/espnet2/speechlm/dataloader/batch.py
cp test_batch_zero.py shim/test_batch_zero.py
cd shim && PYTHONPATH=. timeout 300 $PY -m pytest test_batch_zero.py -q 2>&1 | tail -12
