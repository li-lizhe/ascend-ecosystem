# espnet#6808 `synchronize_batches()` — `device is None` 分支可达性验证 + 显式报错修复（2026-09-26）

> 归属：espnet/espnet 非 PyTorch 主仓，故本记录归**昇腾生态适配**（`ascend-eco-repo/projects/espnet/`），
> **不放进** `mindlog/log` 的 `特性解耦L2/`（那个目录专供 PyTorch 解耦工作）。
> 触发：维护者 `sw005320` 在 PR #6808 上提出 review 问题，用户指示「先验证，把证据准备充分；如果可达，按照建议显式报错」。

## 0. 一句话结论

`dist.is_initialized() == True` 而 `_current_accelerator_device() is None` **确实可达**（真机复现：gloo 进程组 + 无 accelerator），
且现状是**静默不同步**（rank 间 batch 数不一致，5 vs 3）。已按维护者建议改为**显式 RuntimeError**，
并验证 accelerator 路径（NPU/HCCL）**行为不变**、上游 23 个单测全通过。

## 1. 背景与对象

| 项 | 值 |
|---|---|
| PR | espnet/espnet#6808 `fix(speechlm): make synchronize_batches work on non-CUDA accelerators` |
| 分支 | `li-lizhe/espnet:fix/speechlm-synchronize-batches-device` |
| 改动文件 | `espnet2/speechlm/dataloader/batch.py`（原 +20 −4） |
| 基线 | base `152fc02` / 修复前 head `b18c225` |
| 维护者原话 | 2026-09-26 02:06 `sw005320`（issuecomment-5842238861） |

维护者两点：

1. **主**：`device is None` 时 `return batches` 是静默跳过 —— 分布式下不同 rank 可能以不同 batch 数继续而不做同步；
   建议显式报错；若 CPU 分布式是有意支持，则应显式处理。
2. **次**：CodeRabbit 指出某 rank 可能在 `synchronize_batches()` 前拿到 0 个 batch；维护者说这是 CUDA 下也存在的既有问题，
   不一定要在本 PR 修，可本 PR 处理或另开跟踪。

## 2. 被测函数（PR 修复后的形态）

```python
def synchronize_batches(batches):
    if not dist.is_initialized():
        return batches
    device = _current_accelerator_device()
    if device is None:
        # No accelerator to run the collective on (CPU-only run).
        return batches          # ← 维护者质疑点
    n_batches = len(batches)
    n_batches_tensor = torch.tensor([n_batches], dtype=torch.long, device=device)
    n_batches_list = [torch.tensor([0], ..., device=device) for _ in range(dist.get_world_size())]
    dist.all_gather(n_batches_list, n_batches_tensor)
    tgt_n_batches = max(t.item() for t in n_batches_list)
    if tgt_n_batches > n_batches:
        batches = batches + batches[-(tgt_n_batches - n_batches):]
    return batches
```

## 3. 环境

- 主机 `192.168.9.177`（A2 / 910B2，主机八卡，容器内可见 4 个设备），容器 `npu-lizhe`。
- conda env `npu215`：Python 3.12.14，`torch 2.15.0.dev20260917+cpu`，`torch_npu 2.15.0.dev20260917+gitec69335`。
- CANN `/opt/ascend/cann-9.2.0-beta.2/set_env.sh`；跑 torch_npu 需 `source set_env.sh` + `LD_LIBRARY_PATH=$CONDA_PREFIX/lib`。
- 工作目录 `/workspace/espnet6808`（`/workspace` 持久化）。
- **被测文件字节一致性**：`batch.py` 从 GitHub contents API 取原始字节，容器内 md5 与 GitHub 原文逐一比对：

  | 文件 | 字节 | md5 |
  |---|---|---|
  | `batch_base.py`（base 152fc02） | 9948 | `dad6d0d9a5b92a0de3c66fdd7a929e94` |
  | `batch_head.py`（PR head b18c225） | 10482 | `072c9915db897c761a716afd8328b8f0` |
  | `batch_fixed.py`（本次修复） | 11146 | `2f87866caa079e1709cdc95b49ce97e3` |
  | `test_batch_fixed.py`（上游单测 + 新增用例） | 7822 | `cec4095388f94aefee278291c60cdc25` |

  三个版本的 `batch.py` 均与 GitHub 原文/待推送内容**逐字节一致**（本地 `==` 比较 + 容器 `md5sum` 双重确认）。

## 4. 验证矩阵与结果

### 4.1 探针 A — `torch.accelerator` 在 NPU 主机上的真实行为

| 条件 | `is_available()` | `current_accelerator()` | `device_count()` | `'torch_npu' in sys.modules` | `_get_privateuse1_backend_name()` |
|---|---|---|---|---|---|
| 不 source CANN 环境，只 `import torch` | **False** | **None** | — | False | `privateuseone` |
| source CANN 环境后，只 `import torch` | **True** | `device(type='npu')` | 4 | True | `npu` |
| 显式 `import torch_npu`（CANN 已 source） | True | `device(type='npu')` | 4 | True | `npu` |

- `TORCH_DEVICE_BACKEND_AUTOLOAD=0`（两种情况都是），所以**不是** torch 的 autoload 机制；观察到的行为是
  「CANN 环境齐备时 `import torch` 即把 torch_npu 带进来」，CANN 缺失时 torch_npu 进不来（显式 import 会因
  `libhccl.so: cannot open shared object file` 失败）。
- `get_default_backend_for_device('npu')` → `hccl`。
- **含义**：在 NPU 主机上，`_current_accelerator_device()` 是否为 `None`，取决于 CANN 环境是否就绪。
  但这不构成本 PR 的现实风险 —— 缺 CANN 时 torch_npu 根本 import 不进来，模型上 NPU 会先在别处硬失败。

### 4.2 探针 B — gloo 进程组（无 accelerator）三态对照【核心证据】

真 2 进程 `torch.distributed.run --standalone --nproc_per_node=2` + `init_process_group(backend="gloo")`，
rank0 给 5 个 batch、rank1 给 3 个：

| 版本 | `dist.is_initialized()` | `_current_accelerator_device()` | rank0 | rank1 | 判定 |
|---|---|---|---|---|---|
| base（改动前） | True (gloo, ws=2) | —（无此函数） | in=5 **out=5** | in=3 **out=3** | **静默跳过，rank 间不一致** |
| head（PR 现状） | True | **None** | in=5 **out=5** | in=3 **out=3** | **仍然静默跳过** |
| fixed（本次修复） | True | None | in=5 → **RuntimeError** | in=3 → **RuntimeError** | **两 rank 一致显式报错** |

- fixed 版本两个 rank 抛**同一条** `RuntimeError`，随后的 `dist.barrier()` **正常通过** ⇒ 没有 rank 卡在集合通信里。
- **对照组（关键）**：同样这套 gloo 设置下，`dist.all_gather` 用 **CPU 张量**跑通，两个 rank 都读到 `[5, 3]`
  ⇒ 「没有 accelerator」**不等于**「集合通信做不了」，静默跳过是一个**策略选择**而非物理限制。
  因此替代方案是把 device 显式取 `torch.device("cpu")`（一行），本次按维护者建议选了报错。

### 4.3 探针 C — NPU/HCCL 回归（修复不能破坏 accelerator 路径）

`source set_env.sh` + 真 2 进程 + `init_process_group(backend="hccl")` + `torch.npu.set_device(rank)`：

| 版本 | `is_available()` / `_current_accelerator_device()` | rank0 | rank1 | 判定 |
|---|---|---|---|---|
| base | True / — | in=5 out=5 | in=3 **out=3** | 未同步（= PR 要修的原始 bug） |
| head | True / `device(type='npu')` | in=5 out=5 | in=3 **out=5** | 已同步（PR 的效果） |
| **fixed** | True / `device(type='npu')` | in=5 out=5 | in=3 **out=5** | **已同步 ⇒ 回归通过** |

三组 HCCL barrier 均 OK。注意 `_current_accelerator_device()` 返回的是**不带 index** 的 `device(type='npu')`，
`torch.tensor(..., device=...)` 接受，collective 正常。

### 4.4 上游单测（byte-identical 测试文件 + 新增用例）

- 上游 `test/espnet2/speechlm/dataloader/test_batch.py` 原文（md5 `bbef021c00f5a350086492f2350338bf`，23 个用例）
  + 新增 `test_sync_initialized_but_no_accelerator`，跑在**最小包壳**上（`espnet2/speechlm/dataloader/{__init__,batch}.py`
  + `PYTHONPATH`，不安装完整 espnet）：

  ```
  23 passed in 0.20s
  ```

- **现有测试的覆盖漏洞**：`test_sync_no_cuda` 只 patch `torch.cuda.is_available=False`，而 CI 里
  `dist.is_initialized()` 本来就是 False，所以它在第一个 `return` 就返回了 ——
  **根本没有覆盖「dist 已初始化 + 无 accelerator」这条分支**（也正是 Codecov 报 patch coverage 23% 的原因）。
  新增用例用 `patch("..._current_accelerator_device", return_value=None)` + `patch(dist.is_initialized, True)`
  覆盖它，且能在**纯 CPU CI** 上跑。

## 5. 可达性结论（回答维护者的「assuming distributed training requires an accelerator here」）

| 路径 | 是否可达 | 依据 |
|---|---|---|
| CPU-only 机器 + gloo 进程组 | **可达** | 探针 B 真机复现（不依赖 mock） |
| espnet 自带训练入口 | **不可达** | `espnet2/speechlm/bin/train.py`：L185 `torch.cuda.set_device(local_rank)` 在进程组之前无条件执行；L191 `deepspeed.init_distributed()` / L195 `init_process_group(backend="nccl")`；L197 `assert dist.is_initialized()` |
| NPU 主机但 CANN 未就绪 | 形式可达 | 探针 A；但该状态下 torch_npu 无法 import，训练会在别处先硬失败 |

⇒ 报错**不会破坏 espnet 任何受支持的运行路径**，同时把「静默不正确」变成「明确失败」。

## 6. 本次改动

```
espnet2/speechlm/dataloader/batch.py
  Notes 段: "- If no accelerator is available, returns batches unchanged"
         → "- If torch.distributed is initialized but no accelerator is available,
            raises RuntimeError (synchronization cannot be performed)"
  device is None 分支: return batches → raise RuntimeError(明确说明 + 提示 CPU 场景的替代做法)

test/espnet2/speechlm/dataloader/test_batch.py
  + test_sync_initialized_but_no_accelerator（patch _current_accelerator_device → None，断言 RuntimeError）
```

推送：commit **`7131ce8825ac0551903c4ccb2d4078b0624b4212`**（parent `b18c225`，2 文件），
推后**逐文件回读比对**：`batch.py` md5 `2f87866caa079e1709cdc95b49ce97e3`、
`test_batch.py` md5 `cec4095388f94aefee278291c60cdc25`，均与本地逐字节一致。
PR head 变为 `7131ce88`，`mergeable=True` / `mergeable_state=blocked`（等 review + CI）。

## 7. 零 batch 问题（维护者第 2 点）

不在本 PR 修（避免扩大 diff），另开跟踪 issue **espnet/espnet#6812**
《speechlm: synchronize_batches() cannot pad a rank that ends up with zero batches》：
`batches[-(tgt_n - n):]` 在 `n_batches == 0` 时切出空列表 ⇒ 该 rank 仍是 0 个 batch，
要么各 rank 步数不一致，要么空 rank 提前退出循环、其余 rank 卡在集合通信上。
建议修法：`all_gather` 之后取 `counts`，`min(counts) == 0` 时全体一致报错（所有 rank 都能看到同一份 gather 结果）。

## 8. 公开动作清单（均已回读确认在线）

| 动作 | 位置 |
|---|---|
| 推送修复 commit | `7131ce8825ac0551903c4ccb2d4078b0624b4212` |
| 回帖（点对点回答 + 披露回归证据） | https://github.com/espnet/espnet/pull/6808#issuecomment-5845160749 |
| 新建跟踪 issue | https://github.com/espnet/espnet/issues/6812 |

## 9. 未做 / 未验证（诚实标注）

- **没有**跑 espnet 的完整单测套件（未安装 espnet）；只把**上游测试文件原文**跑在最小包壳上（23 passed）。
- **没有**跑完整 SpeechLM 训练；只跑被测函数本身。
- CUDA/XPU 的 accelerator 路径**未在真机验证**（本机无 CUDA 设备）；但本次改动只在 `device is None` 分支加异常，
  `device is not None` 的代码路径逐字未改。
- 「NPU 主机上 `torch.accelerator.is_available()` 取决于 CANN 环境」的**底层机制未追到源码**（只确认了
  `TORCH_DEVICE_BACKEND_AUTOLOAD=0`，故不是该机制），此处只报可观测行为。
- 探针 C 的 base 组 rank0 输出 `out=5 expected_out=5 -> OK` 是**假通过**：rank0 本来就有 5 个 batch，
  未同步也看不出差别；真正体现差异的是 rank1 的 `out=3`。判定必须看 rank1。

## 10. 证据文件

`C:\Users\华为\ascend-eco-repo\projects\espnet\evidence-20260926\`

- `batch_base.py` / `batch_head.py` / `batch_fixed.py` — 三个版本的被测文件（与 GitHub 原文逐字节一致）
- `test_batch_upstream.py` / `test_batch_fixed.py` — 上游单测原文 / 加新增用例后
- `probe_accel.py` / `probe_env.py` / `probe_gloo.py` / `probe_npu.py` / `scan_envs.py` — 探针
- `run2.sh` / `run3.sh` / `run4.sh` — 运行脚本
- `results.txt` — 三段探针的完整原始输出

---

## 11. 第二轮（同日）：review 第 2 点「零 batch」→ 姊妹 PR #6813

### 11.1 起因与判断

- 维护者 `sw005320` 原话：「Also, CodeRabbit points out that a rank can potentially end up with zero batches
  before `synchronize_batches()`. This appears to be a pre-existing issue for CUDA as well, so I don't
  necessarily think it needs to be fixed in this PR, but it would be good to **either handle it here or track
  it separately**.」
- CodeRabbit 行内意见（`batch.py:296`）原话：「**Handle zero-batch ranks before padding.** … Add a consistent
  cross-rank validation error for zero batches, or define and implement a valid empty-rank or synthetic-batch
  contract.」
- 处置：**另开 PR**（不塞进 #6808 扩大 diff），基于 `master` 保持独立可合。

### 11.2 修的时候又发现第二个 bug（同一段代码）

`batches = batches + batches[-(tgt_n_batches - n_batches):]` —— 当 `n_batches < tgt_n_batches - n_batches`
（该 rank 的 batch 数不到最大值一半）时切片长度不够，**补齐后仍然对不齐**：

| n | tgt | 原式结果 | |
|---|---|---|---|
| 1 | 3 | 2 | 仍然短 |
| 2 | 5 | 4 | 仍然短 |
| 2 | 4 | 4 | OK |
| 3 | 5 | 5 | OK |

（纯 Python 切片语义即可判定，随后在真机上以 n=2/tgt=5 复现，见 `results_round2.txt` A/B 段。）
⇒ 「各 rank 以不同 batch 数继续」不只是零 batch 的问题，这条是**没人报过**的。

### 11.3 改动（`batch.py` +26/−2）

1. `all_gather` 后取 `batch_counts`；`tgt_n_batches > 0 and min(batch_counts) == 0` → 全体 rank 同一条
   `RuntimeError`（所有 rank 看到同一份 counts，天然一致，且在 padding **之前**）。
2. 补齐改为循环尾部：`tail = batches[-n_missing:] if n_missing <= n_batches else batches` +
   `list(islice(cycle(tail), n_missing))`（新增 `from itertools import cycle, islice`）。
3. docstring 补 `Raises:` 段与 Notes。
4. 新增 3 条单测（纯 CPU 可跑）：`test_sync_pads_short_rank_fully` /
   `test_sync_zero_batches_on_some_rank` / `test_sync_all_ranks_empty`。

### 11.4 真机验证（910B2；gloo 与 hccl 结果完全一致）

| counts(rank0,rank1) | 改动前 | 改动后 |
|---|---|---|
| 5, 0 | rank0=5 / rank1=0（静默，无报错） | 两 rank 同一条 `RuntimeError` |
| 5, 2 | rank0=5 / rank1=**4** | rank0=5 / rank1=5 |
| 5, 3 | rank1=5（原路径） | rank1=5（不变） |
| 0, 0 | no-op | no-op（不误报） |

报错后 `dist.barrier()` 仍通过 ⇒ 不会把一个静默错误换成一个挂死。
上游单测原文 + 新增 3 例 = **25 passed**（上游原有 22 例）。

### 11.5 诚实标注（这一轮特有）

master 版 `synchronize_batches()` 有**两处 CUDA 硬绑定**：`torch.cuda.is_available()` 门 + `device="cuda"`。
在无 CUDA 的测试机上，这两者不重映射则该分支**根本不可达**、逻辑无法被触发。探针**只**重映射「设备字符串
cuda」与 CUDA 可用性门（把模块的 `torch` 换成只改 device 的 `SimpleNamespace`），**被测函数体逐字节原样**，
集合通信是真实 gloo/hccl。#6808 合入后该门被移除，本逻辑即可在任何加速器上原样运行 —— 届时这两处重映射
都不再需要。新单测里用同一手法（`_fake_dist()` 只重映射 device），因为 CI 无 CUDA。

### 11.6 提交与回读

| 项 | 值 |
|---|---|
| 分支 | `li-lizhe/espnet:fix/speechlm-synchronize-batches-zero-batch` |
| commit | `38f3d2784f9d5ad99a9a7f1ac74d0ed27a7e28d3`（parent `152fc02` = master head） |
| PR | https://github.com/espnet/espnet/pull/6813 —— open / mergeable=True / 1 commit / 2 files (+79/−2) |
| 回读 | `batch.py` online=aac5311256e4 local=aac5311256e4 OK；`test_batch.py` online=28057d13278d local=28057d13278d OK |
| 回帖 | [#6812](https://github.com/espnet/espnet/issues/6812#issuecomment-5845657932) 关联 PR；[#6808](https://github.com/espnet/espnet/pull/6808#issuecomment-5845658397) 告知「单独跟踪」已落成 PR |

### 11.7 证据文件（第二轮）

`C:\Users\华为\ascend-eco-repo\projects\espnet\evidence-20260926-pr6813\`

- `batch_master.py`（上游 master 原文）/ `batch_zero.py`（本 PR 推送内容）/ `test_batch_zero.py`
- `probe_zb.py` / `run_zb.sh` / `run_zbB.sh`
- `results_round2.txt` — gloo + HCCL + 单测 + 回读的完整原始输出
