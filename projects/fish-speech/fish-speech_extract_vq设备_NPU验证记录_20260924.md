# fish-speech extract_vq 设备硬编码修复 — NPU 验证记录 (2026-09-24)

> 过程文档（归档：昇腾生态适配 `ascend-eco-repo/projects/fish-speech/`；非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`）。
> PR: https://github.com/fishaudio/fish-speech/pull/1339 · 自建 issue: https://github.com/fishaudio/fish-speech/issues/1338

## 1. 目标与选型

- 项目：`fishaudio/fish-speech`（32.8K★，国产 TTS，非华为系）
- 活跃度：pushed 2026-09-16（8 天前），14 天内 1 个 PR 合入 → **过活项目硬门槛**（最近有人 merge）
- 从未投过 PR；仓库有 NPU 需求痕迹：issue #1128「How to change CUDA to NPU」(closed)
- 本轮先按「无现成 open issue → 自建 issue」流程建了 #1338，再提 PR 引用 `Fixes #1338`

## 2. bug 定位

`tools/vqgan/extract_vq.py`（VQ 码本抽取工具，训练数据准备必跑）第 108 行：

```python
wav = torchaudio.functional.resample(wav.cuda(), sr, model.sample_rate)[0]
```

但同一个函数往下两行就已经在用 `model.device`：

```python
audio_lengths = torch.tensor(audio_lengths, device=model.device, dtype=torch.long)
```

而 `get_model(config_name, checkpoint_path, device=...)` 本来就接受 `device` 参数。
即：**调用方可以把 codec 放到任意设备，但音频被无条件搬到 CUDA** —— 非 CUDA 后端
（昇腾 NPU / MPS / CPU）上 `.cuda()` 直接抛 `AssertionError: Torch not compiled with CUDA enabled`。

修法（+3/-1，纯 device 传递，不引入 `if npu:`，也不写 cuda/cpu 二选一）：

```python
wav = torchaudio.functional.resample(wav.to(model.device), sr, model.sample_rate)[0]
```

## 3. 真机环境

同 OpenRLHF 轮：`root@192.168.9.177` → 容器 `npu-lz2409`（`dcp-dev-test:latest`），
`/opt/npu-pytorch-setup/venv_npu/bin/python3`，torch 2.13.0a0 + torch_npu，8×Ascend910B2。

**限制**：容器内 **无 torchaudio**，故 `torchaudio.functional.resample` 本身未被执行——
被测改动是纯 device 传递（resample 本身 device-agnostic），探针用 stub codec 复现
`process_batch` 的设备流向。

## 4. 探针与输出

探针 `_fs_vq_probe.py`：
- BEFORE：`wav.cuda()`（原样）
- AFTER：`wav.to(model.device)`，并做真实 NPU 计算（stub codec 的 Conv1d encode）
  与 CPU 参考对比

```
torch 2.13.0a0+gitfad7424 | npu available: True
BEFORE (wav.cuda()): AssertionError: Torch not compiled with CUDA enabled
AFTER (wav.to(model.device)): audios.device=npu:0 lens.device=npu:0
AFTER: model.encode() on NPU ok -> feature_sum=12057.5059 total_len=16000
AFTER: NPU result matches CPU reference (rtol=1e-3): True [npu=12057.5059 cpu=12057.5029]
```

→ 修复前在 NPU 上必崩；修复后张量落在 npu:0、NPU 上前向跑通、结果与 CPU 一致。

## 5. 诚实边界（PR body 已写明）

- **没测**：`torchaudio.functional.resample` 本体（容器无 torchaudio）
- **没测**：完整 CLI（需要 codec checkpoint `checkpoints/openaudio-s1-mini/codec.pth`）
- `get_model()` 的 `device="cuda"` 默认值、`main()` 未暴露 `--device` 参数**未改**，
  在 PR 里明确写成「独立的后续项」，不夹带

## 6. 提交后观察

- PR 建好后 **pre-commit-ci[bot] 自动追加了一个格式化 commit**（`cd50f49ab6`），
  把我那一行按 88 列折成 3 行 → 说明该仓库的 pre-commit 会在 PR 上自动跑。
  语义不变，diff 变 +3/-1。后续同类改动可直接按 ruff 88 列折行，省一次 bot 提交。

## 7. 本轮被否掉的候选（避免下轮重走）

- **OpenVoice（37.6K★）**：pushed 2025-04-19，14 天 0 合入 → 僵尸，弃。
  （虽有 `openvoice/api.py` `device='cuda:0'` 默认 + `assert torch.cuda.is_available()` 的干净硬编码）
- **albumentations（13K★）**：14 天 0 合入 → 僵尸，弃。
- **huggingface/lerobot（27.7K★）**：**已投过 PR**（#4676 closed / #4677 open / #4678 open 均为 li-lizhe）
  → 属促活 job 职责，探新跳过。
- **ragflow（91K★，518 合入/14 天）**：全仓仅 3 处 `torch.cuda`（`common/settings.py:518`、
  `deepdoc/vision/ocr.py:93`、`t_ocr.py:38`），且已有 `ais_bench` 的 Ascend 推理路径
  （`AscendLayoutRecognizer` / `_run_ascend_tsr`）→ 无干净 NPU 崩溃点，保留候选。
- **sherpa-onnx（14.9K★，17 合入/14 天）**：Python 层 435 个 py 文件 **零** device 硬编码；
  最像样的平台 bug #3885（Windows 非 ASCII 路径）已被 modelpath-dev 认领 → 跳过。
- **msdetection / Wan2.1 / HunyuanVideo**：14 天 0 合入，僵尸。
- **fish-speech 的 NPU RNG 假设被真机证伪**（重要，避免下轮重复）：
  曾怀疑 `fish_speech/utils/utils.py:set_seed` 只 seed CUDA RNG，NPU 上 `--seed` 不可复现。
  真机实测：仅 `torch.manual_seed(42)` 后 `torch.randn(4, device="npu")` 三个独立进程输出**完全一致**
  → 该 torch_npu 版本下 `torch.manual_seed` 已同步 NPU generator，**不是 bug**，撤掉。
  （另注：`torch.multinomial` 在 910B2 上对全零 logits 抛 aicpu 异常 507018，属 torch_npu/CANN 侧，
  不适合作为上游 PR 目标。）
