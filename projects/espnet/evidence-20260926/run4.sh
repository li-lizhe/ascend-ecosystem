#!/bin/bash
PY=/opt/miniconda/envs/npu215/bin/python
cd /workspace/espnet6808
echo "########## (a) 不 source CANN 环境 ##########"
$PY probe_env.py 2>&1 | grep -viE "futurewarning|current_device_index"
echo
echo "########## (b) source CANN 环境后 ##########"
source /opt/ascend/cann-9.2.0-beta.2/set_env.sh
export LD_LIBRARY_PATH=/opt/miniconda/envs/npu215/lib:$LD_LIBRARY_PATH
$PY probe_env.py 2>&1 | grep -viE "futurewarning|current_device_index"
