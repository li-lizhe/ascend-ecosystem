# FunASR · 昇腾 910B 适配

达摩院语音识别工具包 [FunASR](https://github.com/modelscope/FunASR) 在昇腾 910B 上「零 torchaudio 依赖」跑通。

## 状态

✅ 代码完成 · ⏳ 上游 PR 待 review

## 问题

FunASR 硬依赖 torchaudio；昇腾 aarch64 + 华为 torch（`2.14.0a0`）无匹配 torchaudio wheel → `import funasr` 即崩。

## 方案 —— 三招去 torchaudio

1. **fbank 特征** → `kaldi-native-fbank` 兜底（新增 shim，保留 torchaudio 优先路径，x86 零影响）
2. **音频加载 / 重采样** → `soundfile` 兜底 + try/except
3. **次要模型 / 数据集顶层 import** → try/except 可选化

## 上游 PR

- **PR #3526（核心）**：Remove hard torchaudio dependency for inference; add kaldi-native-fbank fbank backend
  https://github.com/modelscope/FunASR/pull/3526 —— 5 文件 `+102/−6`
- **PR #3527（扩展）**：Make torchaudio import optional in paraformer_v2, fun_asr_nano and dataset preprocessors
  https://github.com/modelscope/FunASR/pull/3527 —— 4 文件 `+18/−5`

Fork：https://github.com/li-lizhe/FunASR

## 验证

- 8× 昇腾 910B2，torch `2.14.0a0+git69231fe`，torch_npu `2.14.0+gitee7bc39`
- paraformer-large：70.47s 音频 → 1.14s 推理，**RTF ≈ 0.0162**（约 62× 实时）
- `import torchaudio` → `ModuleNotFoundError`（真实零依赖验证）

## 关联

- 教程：[FunASR 在昇腾 910B 上零 torchaudio 跑通](../tutorials/funasr-on-ascend-910b/README.md)
- 可复用件：[fbank shim](../shared/fbank_kaldi_native_fbank.py)、[去 torchaudio checklist](../shared/torchaudio-free-checklist.md)