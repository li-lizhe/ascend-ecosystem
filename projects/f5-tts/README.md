# F5-TTS 昇腾适配

## 问题

`src/f5_tts/eval/utils_eval.py` 在英文 ASR 评估路径中硬编码 `device="cuda"` 与 `compute_type="float16"`，导致在 CPU、Apple Silicon、Ascend NPU 等非 CUDA 环境下直接崩溃。

## 修复

PR #1318：检测 `torch.cuda.is_available()`，CUDA 存在时保持原行为，否则回退到 `cpu` + `int8`。

## 验证

- 在 CPU-only 环境调用 `load_asr_model("en")` 不再因 CUDA 不可用而崩溃。
- 未在 NPU 真机完整跑通 WER 评估（缺少 faster-whisper 在 NPU 上的完整安装）。
