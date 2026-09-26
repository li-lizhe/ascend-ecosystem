# timm（huggingface/pytorch-image-models）设备绑定漏非 CUDA 分支 — NPU 验证记录

> 归档：昇腾生态适配 `ascend-eco-repo/projects/timm/`；非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`。
> PR: https://github.com/huggingface/pytorch-image-models/pull/2801 · 自建 issue: https://github.com/huggingface/pytorch-image-models/issues/2800
> 来源：2026-09-23 晚 21 点探新流水线（**选型驱动扫描**，非 issue 认领：先拉 tarball 静态扫 device 硬编码，再上昇腾真机验证）。同轮另一目标见 [`../DiffSynth-Studio/`](../DiffSynth-Studio/)。

## 1. 定位

`timm/utils/distributed.py:173`（`init_distributed_device_so`）

```python
    if device_type == 'cuda':
        assert torch.cuda.is_available(), ...
    if device_type == 'npu':
        assert torch.npu.is_available(), ...          # 已有 NPU 分支
    ...
    if distributed and device != 'cpu':
        device = f'{device_type}:{local_rank}'        # npu -> 'npu:3'

    if device.startswith('cuda:'):                    # ← 只绑 CUDA
        torch.cuda.set_device(device)
```

timm 其实**已部分支持 NPU**（`timm/data/loader.py:127 self.is_npu`、`train.py:1417 elif device.type == 'npu'`、
`distributed.py:163 assert torch.npu.is_available()`），唯独设备绑定这一步漏了非 CUDA 分支。

## 2. 真机复现（修复前，单进程直调）

投递内容：真实 `timm/utils/distributed.py`（逐字节原样）+ 空 `__init__.py` + stub `unwrap_model`
（完整包需要 torchvision，容器没有；被测函数不使用 `unwrap_model`）。

```
[env] torch 2.15.0.dev20260917+cpu | npu avail True | count 8
[before] torch.npu.current_device() = 0
[resolved] device = npu:3 | distributed = False
[after]  torch.npu.current_device() = 0          ← 指定的 npu:3 被忽略
[impact] torch.ones(device='npu').device = npu:0 | sum = 4.0
```

影响：8 卡机器上 `python train.py --device npu:3`、以及 torchrun `--device npu`（每 rank 被改写成
`npu:<local_rank>`）全部落在 NPU 0 —— 所有 rank 挤一张卡（OOM / 结果错），而返回的 device 字符串却声称是 npu:3。

## 3. 修复后（单进程）

```python
    if device.startswith('cuda:'):
        torch.cuda.set_device(device)
    elif device.startswith('npu:'):
        torch.npu.set_device(device)
```

```
[before] torch.npu.current_device() = 0
[resolved] device = npu:3 | distributed = False
[after]  torch.npu.current_device() = 3          ← 绑定成功
[impact] torch.ones(device='npu').device = npu:3 | sum = 4.0
```

diff：+2/−0 行，纯 device-agnostic（对 cuda/cpu 用户零行为变化）。

## 4. 多卡分布式真机验证（2026-09-24，闭环单进程验证的缺口）

**起因**：维护者 rwightman 在 PR 上直问「did you actually try distributed training or run train with a
'npu:3' without and observe activity on the wrong NPU?」→ 补真机多卡验证。

**方法**：真实 `torchrun --nproc_per_node=4`（HCCL backend，169 / 容器 `npu-lerobot` / 8×910B4），
同一脚本跑两遍 —— before = 上游 `0df212b` 的 `timm/utils/distributed.py`，after = PR head `82f6551`，
两个文件**逐字节原样**（md5 `f9b64cd0…` / `35923d06…`，传输后回读校验）。
脚本内容：`init_distributed_device_so(device='npu')` → 真实 HCCL `all_reduce` → 真实 DDP 前反向
（128→128→4 小模型）→ 可选 512MB 裸 `'npu'` 标记张量（`BIG_MB`）→ 可选 `HOLD_SECS` 保活，
供宿主机 `npu-smi` 采样跨进程 HBM 落点。

**per-rank 观测（4 rank，两次 all_reduce 均得 10.0 = 1+2+3+4，DDP step 均 ok）**

| 观测项 | 上游 0df212b | 本 PR 82f6551 |
|---|---|---|
| `torch.npu.current_device()` | 0, 0, 0, 0 | 0, 1, 2, 3 |
| `torch.ones(4, device='npu').device`（裸 `'npu'`） | npu:0 ×4 | npu:0 / 1 / 2 / 3 |
| 返回的 `device` 字符串 | npu:0..3 | npu:0..3 |
| `ddp_param_device`（显式 `.to(resolved)`） | npu:0..3 | npu:0..3 |

**宿主机 HBM 落点（`npu-smi` 每卡 HBM，相对同配置空载基线）**

| 配置 | NPU0 | NPU1 | NPU2 | NPU3 |
|---|---|---|---|---|
| 上游，BIG_MB=0（对照，隔离 HCCL/运行时开销） | +688 | +493 | +494 | +492 |
| 上游，BIG_MB=512/rank | **+2744** | +493 | +492 | +492 |
| 本 PR，BIG_MB=512/rank | +1007 | +1007 | +1007 | +1007 |

→ 上游配置下，4 个 rank 的 512MB **全部落在 NPU0**（NPU0 相对对照多出 2056MB ≈ 4×512，NPU1/2/3 零增量）；
打补丁后每卡各 +514MB（= 各自 rank 一张）。「所有 rank 挤 NPU0」被真实量化复现。

**结论（诚实口径）**

- 「错卡」真实且可复现，但**只影响读隐式 current device 的代码**：裸 `device='npu'`、`device=None` 兜底、
  训练循环里调用的第三方库；timm 自己的 `train.py/validate.py` 处处显式传 `device:index`，
  `.to('npu:N')` 路径修复前后都正确，DDP/HCCL 两次都正常。
- **附带发现**：HCCL 通信上下文（每 rank ~490MB）本来就按 `LOCAL_RANK` 落到各自卡上（HCCL 自己读
  `LOCAL_RANK`，与 torch 的 current device 无关）——这正是「单进程直调看起来没问题、多卡却真有错放」的原因，
  也是集合通信不受影响的原因。
- 本次**仍未**跑 timm 的 `train.py` 端到端（容器无 torchvision / 无数据集），跑的是「真实多进程 torchrun +
  真实 HCCL 集合通信 + 真实 DDP 训练步」，被测函数与真实训练同路径。此边界已在 PR 评论中写明。
- 已把该证据作为英文评论回复 rwightman（comment 5805110008，2026-09-24T00:15Z），并把「是否保留」交其定夺。
- 无 CUDA 机器，未验证 CUDA 分支（新语句对非 `npu:` 前缀设备是 no-op）。

## 5. 真机环境（169）

```
服务器   root@192.168.9.169   （ssh -i C:\Users\华为\.ssh\id_ed25519）
容器     npu-lerobot
python   /opt/miniconda/envs/npu/bin/python
CANN     source /usr/local/Ascend/ascend-toolkit/set_env.sh
torch    2.15.0.dev20260917+cpu
torch_npu 2.15.0.dev20260917+gitec69335
NPU      8 × Ascend910B4（torch.npu.is_available()=True, device_count()=8）
投递方式 cat pkg.tgz | ssh ... "docker exec -i npu-lerobot bash -lc '...'"
```

## 6. 本轮踩坑（通用，另一目标同样适用）

1. **仓库改名**：`/search/issues?q=repo:rwightman/pytorch-image-models+...` 一律返回 `Validation Failed`
   —— 仓库已改名到 `huggingface/pytorch-image-models`。不是 token 失效、不是限流。codeload 走旧名仍 302 成功，
   所以「能拉到源码」≠「仓库名还对」。**查重前先 `GET /repos/<o>/<r>` 核 `full_name`。**
2. **stdin 被吃掉**：`cat a.py b.py | ssh ... "bash -lc 'cat > b.py'"` 会把**两个文件**都灌进 b.py。多文件一律打成 tgz 再管道投递。
3. **脚本内 `sys.path` 写死**：测试脚本里 `sys.path.insert(0, '/tmp/timmtest')` 写死后，改投到 `/tmp/timmfix`
   仍加载旧目录的旧文件 → 修复后现象不变、差点误判修复无效。改成 `os.path.dirname(os.path.abspath(__file__))`。
4. **多租户 AICore 争用**：首次带 forward 的脚本 300s 超时（假 hang）。加 `NPU_AUTOTUNE_MAX_CONFIGS=1` + `timeout`，
   并把崩溃复现与 forward 拆成两段后正常。
5. **时间戳**：本机时钟比容器快约 233s，`tar xzf` 打印 `time stamp ... in the future` 警告，不影响解包，可忽略。

## 7. 后续可挖（本轮扫描所得，未提交）

- `timm/utils/cuda.py` NativeScaler（`device='cuda'` 默认 + `torch.cuda.amp.GradScaler()` 兜底）
- `timm/optim/_optim_factory.py:206,212` 的 apex/bnb `assert torch.cuda.is_available()`

## 8. 提交动作

| 项目 | issue | PR | 分支 | diff | 验证等级 |
|------|-------|----|------|------|---------|
| huggingface/pytorch-image-models | #2800 | [#2801](https://github.com/huggingface/pytorch-image-models/pull/2801) | `fix/npu-set-device-distributed` | +2/−0 | 🔴 真机 910B4 |

提交流程：fork（API）→ 上游 main sha 建分支 → `PUT contents`（base64 走临时文件，规避 Windows 32K 命令行上限）→
`POST pulls`（head 必须 `li-lizhe:<branch>`）→ 回读 PR 校验 diff。PR 均 `state=open`，无 bot 关闭、无 CLA 阻塞。
**注意：本项目 PR 尚未纳入 `PRS.md` 跟踪表。**
