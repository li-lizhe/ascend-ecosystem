# ai-toolkit · 昇腾 910B 适配

[ostris/ai-toolkit](https://github.com/ostris/ai-toolkit)（约 1.2 万 star，Ostris）—— LoRA/微调训练工具包（FLUX/SD/Qwen 等）。修复其 torchaudio 硬依赖，让非音频路径在无 torchaudio 的昇腾/ARM aarch64 平台可用。

## 状态

✅ PR #1022 已提交（open，等 review）：torchaudio 可选化 + captioner librosa 兜底（2026-08-29）。

## 问题

- `toolkit/config_modules.py:7` 顶层 `import torchaudio`，但 torchaudio 不在 requirements.txt —— 新环境/无 wheel 平台（Linux aarch64 无 torchaudio wheel）任何训练任务启动即 `ModuleNotFoundError`（#415、#436，均为 closed 未修复的用户崩溃报告）。
- `toolkit/audio/preserve_pitch.py`、`extensions_built_in/captioner/AceStepCaptioner.py` 同样顶层硬 import。
- 注意：requirements 有 `torchcodec==0.9.1`（音视频用），但 torchaudio 本体缺失；manager/env.py 的 torch_stack() 早已把 torchaudio import 失败视为可容忍状态（"ERROR: ..."），说明作者本意即允许 torchaudio 缺失。

## 修复（3 文件 +46/−12）

1. 三处顶层 import 改 `try/except Exception: torchaudio = None`（Exception 而非 ImportError，覆盖 wheel 在但原生库加载失败的坏安装）。
2. `config_modules.py` 音频保存分支：torchaudio 缺失时 raise 可操作的 RuntimeError（提示 pip install torchaudio），而非裸 ModuleNotFoundError。
3. `AceStepCaptioner.py` 新增 `load_audio_mono()`：torchaudio 可用走原生，否则 librosa（该文件 BPM/调性分析本就硬依赖 librosa）load+mono+resample；转写路径改用它。

与 open PR #1000（把 torchaudio 加进 requirements）互补：#1000 服务有 wheel 平台，本 PR 保证无 wheel 平台 + 非音频任务不受影响。

## 验证（昇腾 910B / aarch64 容器 npu-lizhe，无 torchaudio）

- `import toolkit.config_modules` / `toolkit.audio.preserve_pitch` 成功，`torchaudio is None`。
- `load_audio_mono()` librosa 兜底：1.5s 立体声 44.1kHz 合成 wav → `(1, 24000)` @16kHz，FFT 峰值 440.0Hz（mono 下混 + 重采样正确）。
- 音频保存路径给出清晰 RuntimeError。
- 验证脚本 `D:\code\mindlog\xql\verify_aitk.py`（容器内 /workspace/aitk_verify）。重依赖（diffusers/optimum/PIL 等）容器内缺失、以 stub 代替 —— 本变更不触及它们。

## 上游 PR

- **PR #1022**：https://github.com/ostris/ai-toolkit/pull/1022 —— head `li-lizhe:optional-torchaudio`，base `main`，Fixes #415 / Fixes #436
- Fork：https://github.com/li-lizhe/ai-toolkit
- 本地仓库：`D:\code\mindlog\xql\ai-toolkit`（分支 optional-torchaudio）

## 社区活跃度（提交前评估）

pushed_at 2026-08-27（1 天前），近期 30 条 closed PR 中 7 条 merged（含单人贡献者小 PR）→ 活跃。
