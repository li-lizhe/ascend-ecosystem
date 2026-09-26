# OpenRLHF loss_utils 设备无关修复 — NPU 验证记录 (2026-09-24)

> 过程文档（归档：昇腾生态适配 `ascend-eco-repo/projects/OpenRLHF/`；非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`）。本轮晚 21 点探新流水线，目标 2 个 PR。
> PR: https://github.com/OpenRLHF/OpenRLHF/pull/1365 · issue 认领: https://github.com/OpenRLHF/OpenRLHF/issues/852

## 1. 目标与选型

- 项目：`OpenRLHF/OpenRLHF`（10.0K★，非华为系，14 天 11 个 PR 合入 → 活项目）
- 从未投过 PR（`check_prs.py` PRS 列表无此 repo）
- 该仓库有 3 个未认领的 NPU 需求 issue：#852「Support for Ascend NPU」、#861「support NPU?」、
  #1016「NPU 训练崩掉」→ 有真实 NPU 用户，且无 maintainer 表态（可下手）

## 2. bug 定位

`openrlhf/utils/loss_utils.py::_optimizer_step_loss_norm`（PPO actor/critic、SFT trainer 都用它）：

```python
device = torch.cuda.current_device() if torch.cuda.is_available() else "cpu"
num_tokens = torch.zeros((), dtype=torch.float32, device=device)
num_samples = torch.zeros((), dtype=torch.float32, device=device)
...
dist.all_reduce(num_tokens, op=dist.ReduceOp.SUM, group=dp_group)
```

两个问题叠加：

1. `torch.cuda.current_device()` 返回的是 **int 索引**，只在 CUDA 上有意义；
2. 非 CUDA 加速器（昇腾 NPU / XPU）走 `"cpu"` 分支 → 标量建在 CPU 上，
   却被送进**设备集合通信**（昇腾 HCCL / CUDA NCCL）→ 直接报错。

同文件 `get_loss_batch_info()` 已经用 `loss_mask.device` 取设备 → 属于**项目内部不一致**，
不是「要求上游支持新硬件」的大工程，因此适合作为小而干净的 PR。

修法（+5/-1）：

```python
device = masks[0].device
```

## 3. 真机环境

- 服务器：`root@192.168.9.177`（169 的 sshd 挂死，banner exchange 超时，177 可用）
- 容器：自建 `npu-lz2409`（镜像 `dcp-dev-test:latest`），宿主 8×Ascend910B2，全部空闲
- 解释器：`/opt/npu-pytorch-setup/venv_npu/bin/python3`
- torch 2.13.0a0+gitfad7424 / torch_npu OK / `npu.is_available()=True` / device_count=8
- 启动命令（宿主机 docker run 需要显式设备 + 无 ascend runtime）：

```
docker run -d --name npu-lz2409 --privileged --shm-size=64g \
  --device=/dev/davinci_manager --device=/dev/devmm_svm --device=/dev/hisi_hdc \
  --device=/dev/davinci0..7 \
  -v /usr/local/Ascend/driver:/usr/local/Ascend/driver:ro \
  -v /usr/local/sbin/npu-smi:/usr/local/sbin/npu-smi:ro \
  dcp-dev-test:latest bash -c "sleep infinity"
```

## 4. 验证方法（多进程 torchrun + 真 HCCL，符合分布式改动硬要求）

- 被测文件 before/after 各一份目录，**同一个脚本只换文件**（`LU_PATH` 环境变量）：
  - `before/loss_utils.py` md5 `6b458cb08773ffa9a44005e04dc54b82`（原样）
  - `after/loss_utils.py`  md5 `881b7056677429b51fb74a921aa4b5c5`（改后）
- 脚本用 `importlib` 加载被测文件，`torchrun --nproc_per_node=2` 起真 HCCL 进程组，
  传 NPU 上的 loss mask（与 trainer 里 `loss_masks.to(device)` 一致）

```
ASCEND_RT_VISIBLE_DEVICES=0,1 torchrun --nproc_per_node=2 _orlhf_probe.py
```

## 5. 实际输出

修复前：

```
[rank 0] dev=npu:0 torch=2.13.0a0+gitfad7424 cuda_available=False npu_available=True
[rank 0] RESULT failed RuntimeError: No backend type associated with device type cpu
[rank 1] dev=npu:1 torch=2.13.0a0+gitfad7424 cuda_available=False npu_available=True
[rank 1] RESULT failed RuntimeError: No backend type associated with device type cpu
```

修复后：

```
[rank 0] RESULT ok batch_num_tokens=32.0 dev=npu:0 global_batch_size=4.0 dev=npu:0
[rank 1] RESULT ok batch_num_tokens=32.0 dev=npu:1 global_batch_size=4.0 dev=npu:1
```

数值自洽：每 rank mask=`ones(4,8)`→32 token、4 条非空样本；2 rank SUM → 64/8，再 `/gas=2`
→ `batch_num_tokens=32.0`、`global_batch_size=4.0`。**且每个 rank 的结果留在自己的卡上**
（rank0→npu:0，rank1→npu:1），不是退回 CPU。

## 6. 诚实边界（PR body 已写明）

- **没测**：端到端 `train_sft.py` / `train_ppo_ray.py` 在 NPU 上跑通（改动只涉及两个标量所在设备，
  已用真 2 rank HCCL all_reduce 覆盖）。
- **没测**：CUDA 行为未回归（逻辑上 `masks[0].device` 与 `torch.cuda.current_device()`
  在 CUDA 上等价，mask 本就在当前设备）。
- 未声称 "works on all backends"。

## 7. 踩坑记录（供后续轮复用）

- **169 sshd 挂死**：`Connection timed out during banner exchange`，从 177 跳板也连不上 → 需重启 sshd。
- **177 上 npu-inductor-base:local 无 torch**；`dcp-dev-test:latest` 才有 torch 2.13+torch_npu。
  `docker exec ... python3` 解析到 `/opt/build-tools/bin/python3`（无 torch），
  **必须用绝对路径 `/opt/npu-pytorch-setup/venv_npu/bin/python3`**。
- 177 无 ascend docker runtime，`--runtime=ascend` 报 unknown runtime；要显式 `--device=/dev/davinci*`。
- 容器里 **无 torchaudio**（本轮第二个 PR 的验证受此限制）。
- 远端 heredoc/引号地狱照旧：一律本地写文件 → `base64 -w0` → `ssh "... | base64 -d > /tmp/x"` →
  `docker cp` → `docker exec`。
- 本机无 `python3`；用 `/c/Users/华为/AppData/Local/hermes/hermes-agent/venv/Scripts/python`。
- tar 打到 MSYS `/tmp` 后原生 `ssh` 读不到（不做路径转换）→ 必须把 tarball 放在
  `$LOCALAPPDATA/Temp/...` 下的原生路径。
