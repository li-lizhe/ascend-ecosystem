# FunASR · 昇腾 910B 适配

达摩院语音识别工具包 [FunASR](https://github.com/modelscope/FunASR) 在昇腾 910B 上「零 torchaudio 依赖」跑通。

## 状态

✅ **已合并**（2026-08-26，by LauraGPT）—— 任务首个成功合入上游的 PR。CHANGES_REQUESTED → 修复 → APPROVED → merged。

## 问题

FunASR 硬依赖 torchaudio；昇腾 aarch64 + 华为 torch（`2.14.0a0`）无匹配 torchaudio wheel → `import funasr` 即崩。
关联上游 issue：#3523（torchaudio 缺失导致的 import 失败 + bare `raise` 掩盖真实异常）。

## 方案 —— 三招去 torchaudio

1. **fbank 特征** → `kaldi-native-fbank` 兜底（新增 shim，保留 torchaudio 优先路径，x86 零影响）
2. **音频加载 / 重采样** → `soundfile`/`librosa` 兜底 + try/except
3. **次要模型 / 数据集顶层 import** → try/except 可选化 + 统一 `torchaudio_compat` guard

## 上游 PR（原 #3526 + #3527 已合并为一个）

- **PR #3526**：Remove hard torchaudio dependency for inference; add kaldi-native-fbank fbank backend
  https://github.com/modelscope/FunASR/pull/3526 —— 10 文件 `+221/−20`（原 5 文件核心 + 原 #3527 的 4 文件已并入）
  - 原 #3527（次要模型 torchaudio 可选化）已关闭，并入本 PR 使改动原子化。

### Review 反馈与修复（LauraGPT, CHANGES_REQUESTED）

| 反馈 | 修复 |
| --- | --- |
| kaldi-native-fbank 未声明依赖，干净环境 import 仍崩 | 加 optional `knf` extra；`fbank()` 调用时无后端才报可操作 ImportError |
| shim `**kwargs` 静默吞参（如 `channel`） | 显式处理 `channel`；`subtract_mean`/`min_duration`/VTLN/`blackman_coeff` 显式 NotImplementedError |
| `forced_align` 宽 except 吞缺失依赖、静默返回空 | 新增共享 guard，依赖缺失时传播 ImportError |
| 未测「torchaudio 完全缺席」环境 | 新增 `tests/test_torchaudio_optional.py` 回归测试 |

Fork：https://github.com/li-lizhe/FunASR

## 验证

- 8× 昇腾 910B2，torch `2.14.0a0+git69231fe`，torch_npu `2.14.0+gitee7bc39`
- paraformer-large：70.47s 音频 → 1.15s 推理，**RTF ≈ 0.0164**（约 61× 实时），fbank 走 kaldi-native-fbank fallback
- `import torchaudio` → `ModuleNotFoundError`（真实零依赖验证）
- 回归测试 `test_torchaudio_optional.py` 在无 torchaudio 环境 10/10 通过

## 关联

- 教程：[FunASR 在昇腾 910B 上零 torchaudio 跑通](../tutorials/funasr-on-ascend-910b/README.md)
- 可复用件：[fbank shim](../shared/fbank_kaldi_native_fbank.py)、[去 torchaudio checklist](../shared/torchaudio-free-checklist.md)