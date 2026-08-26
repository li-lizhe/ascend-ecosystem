# Roadmap · 后续规划

按「能力复用优先、低门槛优先」排序的候选池，将**逐项处理**：评估 → 适配 → 验证 → 上游 PR → 写教程。

## 候选池

> 优先级待定，欢迎 issue 提名。每个项目处理完即移入 `projects/` 并在 README 登记。

| # | 项目 | 方向 | 适配点 | 依据 |
|---|------|------|--------|------|
| 1 | FunASR 家族新模型（SenseVoice / GLM-ASR / Qwen3-ASR） | 语音识别 | 复用去 torchaudio 方案 | 同一仓库，能力直接复用，见效快 |
| 2 | CosyVoice | 语音合成 | 去 torchaudio + NPU 推理验证 | 同为 ModelScope 生态 |
| 3 | Sherpa-ONNX / k2-fsa 生态 | 语音 | fbank 结果一致性对照 | 与 kaldi-native-fbank 同源 |
| 4 | Faster-Whisper（CTranslate2） | 语音识别 | 纯 C++ 后端昇腾适配 | 关注度高的 ASR 项目 |
| 5 | vLLM / llama.cpp 昇腾后端 | 通用 LLM 推理 | 国产算力规模化推理 | 拓到 LLM 方向 |

## 状态标记

- 🔭 待评估 · 🚧 适配中 · ✅ 已完成 · ❌ 暂缓（附原因）

## 逐项处理流程

1. 调研该项目在 aarch64 + 华为 torch 环境的坑
2. 出最小改动方案（设备无关、最小侵入）
3. 910B 实机 E2E 验证 + 性能数据（RTF 等）
4. fork + 提 PR（小量多次分批，便于 review）
5. 写推广教程 + 更新本仓库

## 当前焦点

- [ ] **FunASR PR review 跟进** —— [PR #3526](https://github.com/modelscope/FunASR/pull/3526) / [#3527](https://github.com/modelscope/FunASR/pull/3527)
- [ ] 候选池 #1（FunASR 家族新模型）评估启动