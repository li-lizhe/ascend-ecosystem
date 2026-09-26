# transformers #48937 compute_stream NPU 验证记录（2026-09-26）

> 归档：昇腾生态适配 `ascend-eco-repo/projects/transformers/`；非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`。

## 0. 一句话结论

评审 IlyasMoutawwakil 问的「能不能一律用 `torch.Stream`」**在 NPU 上答案是「能」**；
但为了回答这个问题去真机验证时，**挖出一个更严重的问题：PR 当前形态在 NPU 上会直接抛
`AssertionError: Torch not compiled with CUDA enabled`** —— 因为 `compute_stream` 的三个消费点
用的是 CUDA 命名空间的 `torch.cuda.stream(...)`。改动已推送（`4107d5b`），评审帖已回。

## 1. 触发

| 项 | 值 |
|---|---|
| PR | huggingface/transformers#48937 `fix: support NPU/XPU compute stream in ContinuousBatchingState` |
| 分支 | `li-lizhe:fix/cont-batch-npu-stream` |
| 评审问题 | `input_outputs.py` 行内：「can't we use torch.Stream always when not cpu ?」（2026-09-21 11:50） |
| 我方 09-24 回复中的**未兑现承诺** | 「I'd like to confirm the NPU dispatch on an Ascend machine first (that's the case this PR is for) and will follow up here.」 |

本次就是把这句话兑现 —— 在昇腾真机上确认 `torch.Stream` 的 NPU dispatch 是否成立。

## 2. 环境

| 项 | 值 |
|---|---|
| 机器 | 177（8×910B2），容器 `npu-lizhe`，`ASCEND_RT_VISIBLE_DEVICES=0` |
| CANN | `/opt/ascend/cann-9.2.0-beta.2/set_env.sh` |
| Python env | `/opt/miniconda/envs/npu215`（Python 3.12.14） |
| torch | `2.15.0.dev20260917+cpu`（**编译时未带 CUDA**，这是后面那个断言的关键） |
| torch_npu | `2.15.0.dev20260917+gitec69335` |
| 验证时的 head | `57bbe67fd1`（即 PR 当时的形态） |

## 3. 探针结果：`torch.Stream` 在 NPU 上可用

| 检查 | 结果 |
|---|---|
| `torch.Stream(device=torch.device("npu:0"))` | ✅ 构造成功，得到基类 `torch.Stream` |
| `torch_npu` 的 Stream 与基类关系 | `torch_npu.npu.streams.Stream` MRO = `[Stream, _NPUStreamBase, Stream(torch), object]` → **torch_npu 的 Stream 是 `torch.Stream` 的子类** |
| `.synchronize()` | ✅ |
| `.query()` | ✅ 返回 True |
| `.record_event()` / `.wait_event(torch.Event())` | ✅ |
| `with torch.Stream(device="npu:0"):` | ✅ **真的切换了当前 stream**（用底层 handle `187651163978200` → `187651172777304` 比对，退出后还原） |
| 该上下文内跑真实 NPU 算子 | ✅ |
| `with torch.npu.Stream(device="npu:0"):` | ✅ 同样切换（handle → `187651173752392`） |
| `torch.npu.stream(<两种 stream>)` | ✅ 都能包住并切换 |
| `torch.accelerator.set_stream(<两种 stream>)` | ✅ 都能切换 |

> 注：对象身份比较（`is`）不可靠 —— `torch.npu.current_stream()` 每次返回新包装对象，
> 所以判定必须用底层 `.npu_stream` handle 比对。

**结论：评审的建议在 NPU 上成立，`torch.npu.Stream` 显式分支不是必需的。**

## 4. 关键发现：PR 当前形态在 NPU 上会崩

`compute_stream` 不只在 `input_outputs.py` 里被消费。全仓检索 `compute_stream` 命中 4 个文件，
其中三处用的是 **CUDA 命名空间**的上下文管理器：

| 文件:行 | 代码 | 是否 NPU 可达 |
|---|---|---|
| `model_runner.py:119` | `maybe_stream = torch.cuda.stream(compute_stream) if compute_stream is not None else nullcontext()` | ✅ 可达（非 CUDA-graph 的 forward 路径） |
| `offloading_manager.py:176` | `_stream_ctx()` → `torch.cuda.stream(self._compute_stream)` | ✅ 可达 |
| `continuous_api.py:618` | `torch.cuda.stream(compute_stream)`（cache copy） | ✅ 可达 |
| `model_runner.py:128/148/153` | CUDA graph replay / capture | ❌ 不可达（graph 路径本身要 CUDA） |

`model_runner.py:119` 一定可达的证据：`cuda_graph_booleans`（`configuration_utils.py:1887`）
在 `use_cuda_graph is None`（默认、自动推断）时返回 `(False, False)` → `use_cuda_graph=False`
→ 走 `if not use_cuda_graph:` 分支 → 命中 119 行。

真机最小复现（910B2，精确复刻 119 行写法）：

```
改动前  compute_stream = None                 -> OK  sum=8.0
改动后  compute_stream = torch.npu.Stream     -> ❌ AssertionError: Torch not compiled with CUDA enabled
评审建议 torch.Stream(device=npu:0)           -> ❌ AssertionError: Torch not compiled with CUDA enabled
```

即：**改动前** NPU 上 `compute_stream is None`，那三处走 `nullcontext()`，不炸；
**改动后** 拿到非 None 的 stream，`torch.cuda.stream` 直接断言失败。
→ 只改构造点是**不够的**，消费点必须一起改成设备无关的写法。

## 5. 顺带发现：`device.type != "cpu"` 这个泛化条件不安全

评审原话是 "always when not cpu"，但真机实测：

```
torch.Stream(device=cpu)   -> OK
torch.Stream(device=npu)   -> OK
torch.Stream(device=meta)  -> OK
torch.Stream(device=cuda)  -> ❌ RuntimeError: PyTorch is not linked with support for cuda devices   (本 build 无 CUDA)
torch.Stream(device=xpu)   -> ❌ RuntimeError: PyTorch is not linked with support for xpu devices
torch.Stream(device=mps)   -> ❌ RuntimeError: PyTorch is not linked with support for mps devices
```

原代码对 mps 等设备是**留 None**（可用的 no-op）；若改成 `elif device.type != "cpu"`，
MPS 上会从「正常工作」变成「init 期抛错」。故只保留真正支持 stream 的加速器。

## 6. 代码改动（已推送 `4107d5b`）

| 文件 | 改动 |
|---|---|
| `utils.py` | 新增 `stream_context(stream)`：None → `nullcontext()`；CUDA → `torch.cuda.stream()`；其余 → 直接返回 stream 本身（`torch.Stream` / 各加速器 Stream 本身就是上下文管理器） |
| `input_outputs.py:120-124` | NPU/XPU 两个分支合并为一个泛化 `torch.Stream` 分支；CUDA 分支保持 `torch.cuda.Stream` 不变 |
| `model_runner.py:119` | `torch.cuda.stream(...)` → `stream_context(...)` |
| `offloading_manager.py:176` | 同上（并清理不再使用的 `nullcontext` import） |
| `continuous_api.py:618` | 同上 |

设计原则：**CUDA 路径逐字不动**（`torch.cuda.Stream` + `torch.cuda.stream`），把回归风险压到零；
只让非 CUDA 加速器走上泛化路径。

## 7. 验证了什么 / 没验证什么（诚实标注）

✅ **验证了**（910B2 真机，torch 2.15.0.dev20260917 + torch_npu 2.15.0.dev20260917）：
- `torch.Stream(device=npu:0)` 的构造、synchronize/query/event、上下文切换、真实算子执行
- 三处消费点在 NPU 上的行为差异（改动前 OK / 改动后 AssertionError）
- `stream_context()` 的三种输入（None / `torch.Stream` / `torch.npu.Stream`）均正确切换并还原
- 各 device.type 下 `torch.Stream(device=...)` 的可用性

❌ **没验证**：
- **CUDA 路径**（本机无 CUDA 设备）—— 但该路径代码逐字未改，且 `stream_context()` 对 CUDA
  stream 返回的就是原来的 `torch.cuda.stream(stream)`，行为等价
- **端到端 continuous batching 生成**（未装该 commit 的 transformers、未跑真实模型）
  → 上面第 4 节是**最小复现**（精确复刻调用点表达式），不是完整 generation 跑通
- **XPU 路径**（无 XPU 设备）
- CI 结果（推完由 GitHub CI 判定）

## 8. 已发出的动作

| 动作 | 结果 |
|---|---|
| 推送修复 | `4107d5b42633cd59014c9b40eb4f9f9a39e63eb7`（分支 `fix/cont-batch-npu-stream`，已回读校验 5 个文件与本地逐字节一致） |
| 修复后处理合并冲突 | `fee5b5754146871701a523507b4bddd2025829e6`（merge main → 分支，见第 10 节） |
| transformers#48937 回帖 | [issuecomment-5844504389](https://github.com/huggingface/transformers/pull/48937#issuecomment-5844504389) —— 回答评审问题 + 披露上述崩溃 + 说明改动 |
| DeepSpeed#8524 ping | [issuecomment-5844504500](https://github.com/deepspeedai/DeepSpeed/pull/8524#issuecomment-5844504500) —— 请维护者 approve workflow run（fork PR 卡在 `action_required`）+ 提示 approve 后有新 commit |
| lerobot#4677 ping | [issuecomment-5844504643](https://github.com/huggingface/lerobot/pull/4677#issuecomment-5844504643) —— ruff format 已完成，请复看 |

## 9. 证据文件

`transformers48937_evidence_20260926/`（与本文件同目录）：
- `probe_stream.py` —— 主探针（构造/协议方法/上下文/等价性 + 不 import torch_npu 对照）
- `probe_no_torch_npu.py` —— 对照：干净进程里 torch_npu 是否已注册
- `probe_stream2.py` —— PR 实际用法（`.synchronize()` 等）+ MRO + 各 API 能否包住
- `probe_stream3.py` —— **复现 `model_runner.py:119`**（本记录第 4 节的核心证据）
- `probe_stream4.py` —— 候选设备无关上下文管理器
- `probe_stream5.py` —— **handle 比对**判定是否真的切换（第 3 节）
- `probe_stream6.py` —— 验证最终 helper + 为何 CUDA 分支必须保留
- `probe_stream7.py` —— 各 device.type 下 `torch.Stream(device=...)` 可用性（第 5 节）
- `patch/` —— 改动后的 5 个文件 + `_orig.json`（改动前原文）

## 10. 后续：分支落后 main 97 个 commit + 合并冲突（已处理）

推完 `4107d5b` 后复查发现两个**新问题**，均已处理：

### 10.1 CI 没跑起来（仅首次推送那个 commit）

`4107d5b` 上只触发了两个 `pull_request_target` 工作流：

| 工作流 | event | 结果 |
|---|---|---|
| PR CI Security Gate | pull_request_target | success |
| PR slow CI - Suggestion | pull_request_target | **failure**（步骤 `Extract PR details` 失败） |

而 `pull_request` 事件的 `PR CI` / `Build PR Documentation` / `Self-hosted runner` **压根没被创建**。
对照：上一个 head `57bbe67f` 上 6 个工作流都创建了（`PR CI` 最终 success）。
→ 该 commit 实际上**没被 CI 覆盖**。原因未定位（无权限取到该 job 日志）。

**注意**：后续 `fee5b575`（merge commit）上 `pull_request` 工作流正常创建了
（`PR CI` / `Build PR Documentation` / `Self-hosted runner` 均为 `action_required`，即 fork PR
待维护者放行 —— 与 `57bbe67f` 当时一致）。所以这更像首次 API 改 ref 的偶发，而非稳定复现。

### 10.2 我的改动引入了合并冲突（PR 原本 mergeable）

复查时 `mergeable_state` 从 `blocked` 变成 **`dirty`**（即冲突）。三方合并预演
（`git merge-file`，只读）确认：分支落后 main **97 个 commit**，冲突 3 个文件：

| 文件 | 冲突位置 | 根因 |
|---|---|---|
| `utils.py` | ~221 行 | 我插入 `stream_context()` 的位置，main 也动了 |
| `model_runner.py` | ~24 行 | 我把 `.utils` import 改成多行，main 也改了同一行 |
| `offloading_manager.py` | ~27 行 | 我删 `nullcontext` import / 加 `.utils` import，main 也动了 |

`input_outputs.py` / `continuous_api.py` 可干净合并。

**这是我的改动造成的**（原 PR 只动 `input_outputs.py` 4 行，本来不冲突），必须由我修掉。

**处理方式**：不是手解冲突标记，而是**把本分支的改动重新施加到 main 的版本上**（main 上这三处
待改字符串与 base 完全一致，替换脚本原样可用），然后建 merge commit
`fee5b5754146871701a523507b4bddd2025829e6`（parents = [`4107d5b`, `main`]）。

**结果**：`mergeable=True`、`mergeable_state=blocked`（不再是 dirty）、`behind_by=0`；
回读校验 5 个文件与本地合并结果逐字节一致；合并后 5 个文件本地语法检查通过。

