#!/bin/bash
cd /workspace/espnet6808
PY=/opt/miniconda/envs/npu215/bin/python
sep(){ echo; echo "########## $* ##########"; }

sep "探针 A: torch_npu 的 import 是否影响 torch.accelerator"
$PY probe_accel.py

sep "探针 B1: base 版 (改动前)"
WHICH=base $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_gloo.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
sep "探针 B2: PR head 版 (当前 PR)"
WHICH=head $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_gloo.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
sep "探针 B3: 修复版 (显式报错)"
WHICH=fixed $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_gloo.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"

sep "探针 C1: NPU/HCCL 回归 - base 版 (改动前, 已知 NPU 上不同步)"
WHICH=base $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_npu.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
sep "探针 C2: NPU/HCCL 回归 - 修复版 (必须仍然同步)"
WHICH=fixed $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_npu.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"

sep "上游单测 (byte-identical test_batch.py + 新增用例) 跑在最小包壳上"
rm -rf shim && mkdir -p shim/espnet2/speechlm/dataloader
touch shim/espnet2/__init__.py shim/espnet2/speechlm/__init__.py shim/espnet2/speechlm/dataloader/__init__.py
cp batch_fixed.py shim/espnet2/speechlm/dataloader/batch.py
cp test_batch_fixed.py shim/test_batch.py
echo "--- 上游原文 vs 修复后, 只应差 batch.py 那一处 + 新增用例 ---"
md5sum batch_fixed.py test_batch_fixed.py
cd shim && PYTHONPATH=. $PY -m pytest test_batch.py -v 2>&1 | tail -45
