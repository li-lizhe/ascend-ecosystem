#!/bin/bash
source /opt/ascend/cann-9.2.0-beta.2/set_env.sh
export LD_LIBRARY_PATH=/opt/miniconda/envs/npu215/lib:$LD_LIBRARY_PATH
cd /workspace/espnet6808
PY=/opt/miniconda/envs/npu215/bin/python
sep(){ echo; echo "########## $* ##########"; }

sep "探针 A: torch_npu 的 import 是否影响 torch.accelerator"
$PY probe_accel.py 2>&1 | grep -viE "futurewarning|current_device_index"

sep "探针 C1: NPU/HCCL - base 版 (改动前, 预期 NPU 上不同步)"
WHICH=base $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_npu.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
sep "探针 C2: NPU/HCCL - PR head 版 (当前 PR, 预期同步)"
WHICH=head $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_npu.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
sep "探针 C3: NPU/HCCL - 修复版 (必须仍然同步 = 回归通过)"
WHICH=fixed $PY -m torch.distributed.run --standalone --nproc_per_node=2 probe_npu.py 2>&1 | grep -viE "warning|future|OMP_NUM|\*\*\*"
