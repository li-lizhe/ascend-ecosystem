# VoiceStudio 设备缓存释放（release_device_cache）NPU 验证记录

- **归档：** 昇腾生态适配 `ascend-eco-repo/projects/VoiceStudio/`（非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`）
- **日期：** 2026-09-23
- **任务：** 促活任务（已合入项目回访）— debpalash/VoiceStudio
- **PR：** [#2317](https://github.com/debpalash/VoiceStudio/pull/2317) `fix(memory): release the device cache on every accelerator the engines can use`
- **分支：** `li-lizhe:fix/device-cache-release-all-accelerators`（fork li-lizhe/VoiceStudio，base=main，3 个 commit）
- **上游基线：** main `453213882dd18c3e8fcca95d0912e7b58a4b4813`（本机无 git clone，走 tarball API 取源码）

## 1. 为什么选 VoiceStudio

促活池里当时没有「距上次合入 >7 天」的项目（最长就是 VoiceStudio / spikingjelly 的 5 天，09-18 合入）。选 VoiceStudio 的理由：

- 空窗最长（与 spikingjelly 并列），且维护者 debpalash **当天仍在合 PR**（09-23 一天合入 4 个）→ 社区活跃、review 响应快。
- 有**不与已合入 #2194 重复**的真实缺陷面（见下）。

## 2. 问题（真机可复现的静默 no-op）

引擎侧车（`backend/engines/{moss_tts_v15,confucius4,dots_tts}/main.py`）用
`torch.accelerator.current_accelerator(check_available=True).type` 选设备，所以在昇腾主机上模型跑在 `npu`。
但 `backend/api/routers/` 里有 **6 处 open-coded 的 CUDA/MPS flush**：

| 文件 | 位置 |
|------|------|
| `api/routers/generation.py` | `_oom_friendly_reraise` |
| `api/routers/dub_generate.py` | `_prepare_oom_retry`、`dub_generate` 内节流的 per-segment release |
| `api/routers/dub_translate.py` | `_unload_nllb`、`_generate_rows` 逐行重试 |
| `api/routers/dub_core.py` | `dub_transcribe_stream`、`dub_transcribe`（**只 flush MPS**） |

```python
if torch.cuda.is_available():
    torch.cuda.empty_cache()
elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
    torch.mps.empty_cache()
```

在 NPU / XPU 主机上这段什么都不做 → allocator 继续持有刚 offload 释放的块 → 下一次分配仍按「已占用」算，OOM 重试白做。

**修法：** 把 `free_vram()` 里已有的窄原语抽成 `services.model_manager.release_device_cache()`，6 处恢复路径改调它；`free_vram()` 保留 gc + cuBLAS 行为。

## 3. 真机验证（Ascend 910B4 ×8）

**通路（skill 已验证路径）：** `ssh -i /c/Users/华为/.ssh/id_ed25519 root@192.168.9.169` → 容器 `npu-lerobot` → `source /usr/local/Ascend/ascend-toolkit/set_env.sh` → `/opt/miniconda/envs/npu/bin/python`

```
torch: 2.15.0.dev20260917+cpu
torch_npu: 2.15.0.dev20260917+gitec69335
torch.cuda.is_available(): False
torch.npu.is_available(): True count: 8 name: Ascend910B4
torch.accelerator.current_accelerator(check_available=True) -> npu | .type = npu
```

**内存计量（`torch.npu.memory_reserved()`，64 MiB 张量分配到 npu:0 后 `del` + `gc.collect()`）：**

```
OLD open-coded CUDA/MPS pair : peak=   134.0 MiB  del+gc=   134.0 MiB  after flush=   134.0 MiB
NEW shared helper            : peak=   134.0 MiB  del+gc=   134.0 MiB  after flush=     0.0 MiB

fail-before (old pair left the cache alone): CONFIRMED
pass-after  (helper released it): CONFIRMED
free_vram() on NPU host ok, reserved now: 0.0 MiB
real NPU compute after flush: 1073741824.0
```

**测试（同一容器，pytest 8.3.2）：**

| 运行 | 结果 |
|------|------|
| `pytest --noconftest -q tests/test_device_cache_release.py tests/test_changelog_style.py tests/test_npu_memory.py`（改动后源码） | **36 passed** |
| 同一测试文件对**改动前**源码树（从 tarball 还原的 4 个 router + model_manager） | **13 failed**（证明测试真能抓回归） |
| `tests/test_dub_remote_safety.py` 的 monkeypatch 机制复刻（patch `torch.cuda.is_available/empty_cache`，helper 读同一 torch 模块） | 三条断言仍成立 |

**未测：** 全量 backend 套件（容器无 fastapi/pydantic/soundfile/librosa，`api/routers/*` 无法 import）；CUDA/MPS/XPU 真机分支（无硬件，仅单测覆盖）；多卡/HCCL 路径未触碰。

## 4. Review 反馈与响应（Greptile bot，两轮）

**第一轮（2 条，均判为成立并修掉）：**

1. **混合设备主机**：CUDA 报可用但推理跑在 XPU/NPU 时，`elif` 链只 flush CUDA → 改成**先问引擎同一问题** `torch.accelerator.current_accelerator(check_available=True)`，flush 该后端；问不出来（pre-2.6 / 驱动探测抛异常）才回退 CUDA/MPS/XPU/NPU 探测链。真机上该分辨率就是 `npu`，验证走的就是这条新路径。
2. **`free_vram()` 失败语义被吞**：改动前它会传播 `empty_cache()` 异常，且 `model_lifecycle` 的卸载调用方把失败报给用户（`success: False, reason: …`）。→ helper 增加 `raise_on_failure` 参数，`free_vram()` 传 `True`；**直接恢复路径仍是 best-effort**（不能因为 flush 失败就让生成请求挂掉）。

改动后追加 commit 3（`8894e657`），并已回帖说明；PR body 的测试数字同步更新为 13/36/13。

## 5. 踩坑记录

- 本机 git HTTPS 仍被墙 → 全程 API 建分支（blob → tree(base_tree=upstream main) → commit(parents=[upstream sha]) → ref → PR）。
- **`curl` 经 stdin 传 body 必须显式 `--data-binary @-`**，否则 GitHub 报 `Validation Failed: content missing_field`（本次踩坑一次）。
- 仓库 CHANGELOG 有硬 linter（`tests/test_changelog_style.py`）：Unreleased 的 Added/Fixed 条目必须带 `(#N)` 或 `— thanks @user!`；仓库惯例是 **ref 在 credit 之前**（`(#2317) — thanks @li-lizhe!`）。开 PR 前还没有 PR 号 → 先 credit-only 过 linter，开完 PR 立刻追加 commit 把 `(#N)` 插进去。
- 改动前**必须查现有测试是否 pin 了旧行为**：`tests/test_dub_remote_safety.py` 正好 patch `dub_generate.torch.cuda.empty_cache`，因 helper 读同一 torch 模块而通过——但要先读确认，不能假设。

## 6. 产物

- PR #2317：3 commit / 8 文件 / +280 −47（源码 66 行改动 + 新增 `tests/test_device_cache_release.py` 13 个用例）
- 已同步：`check_prs.py` PRS 列表、`references/incubated-projects.md`（VoiceStudio → ⏳ open #2317）、`references/project-memory.md`
