# WhisperX · 昇腾 910B 适配

[m-bain/whisperX](https://github.com/m-bain/whisperX)（约 2.4 万 star，Oxford Max Bain）—— 时间精准的自动语音识别（Whisper + word/字符级 forced alignment + 说话人分离）。修复其 torchaudio 硬依赖，让 alignment 在无 torchaudio 的昇腾/ARM aarch64 平台可用。

## 状态

✅ PR #1469 已提交（open，等 review）：torchaudio 可选化 + Hugging Face 兜底。
- 2026-08-27 Copilot bot review（COMMENTED，4 条建议）。
- 2026-08-29 已全部处理并推送 51ca65b：import guard 改为 `except Exception`、中文注释译英、新增 fallback 行为单测（monkeypatch torchaudio=None，验证 bundle 名重映射到 HF checkpoint）。昇腾 910B 上 3/3 测试通过，已在 PR 回复说明并请求 re-review。

## 问题

- `whisperx/alignment.py` 顶层 `import torchaudio`（硬依赖）；`pyproject.toml` 硬 pin `torchaudio~=2.8.0`。
- PyTorch 官方 **无 Linux aarch64 的 torchaudio wheel**，昇腾（华为 torch 版本与官方脱钩）+ 鲲鹏 ARM 环境 `pip install whisperx` 直接失败，import `whisperx.alignment` 也崩。
- torchaudio 在 whisperX 里唯一用途 = `torchaudio.pipelines` 加载 wav2vec2 对齐模型（en/fr/de/es/it 五个默认语言），其余 30+ 语言本就走 Hugging Face。

## 修复（3 文件 +42/−3，远小于 200 行）

1. `whisperx/alignment.py`：`import torchaudio` 改 `try/except ImportError`（可选化）。
2. 新增 `TORCHAUDIO_PIPELINE_TO_HF` 映射：五个 torchaudio.pipelines 模型 → 等价 HF checkpoint（`WAV2VEC2_ASR_BASE_960H` → `facebook/wav2vec2-base-960h` 等）。torchaudio 缺失时，默认 en/fr/de/es/it 自动兜底到 HF。
3. `pyproject.toml`：`torchaudio` 从 `dependencies` 移到可选 extra `align-torch`（只有走 torchaudio.pipelines 路径才需要）。
4. `tests/test_align_model_fallback.py`：回归测试，保证映射不再遗漏。

## 验证（昇腾 910B / aarch64 容器，无 torchaudio）

- 环境：npu177 / npu-lizhe，torch `2.14.0a0+git69231fe` + torch_npu（4 卡），transformers 5.15.1 / pandas 3.0.5。
- `import whisperx.alignment` 成功，模块内 `torchaudio = None`。
- `TORCHAUDIO_PIPELINE_TO_HF` 五个默认 torch 模型全部映射到 `facebook/...`；36 个 HF 默认语言不受影响。
- **验证为 import + 映射逻辑级**（未做完整模型下载+推理 E2E，见下）。

## 上游 PR

- **PR #1469**：https://github.com/m-bain/whisperX/pull/1469 —— head `li-lizhe:fix-optional-torchaudio`，base `main`
- Fork：https://github.com/li-lizhe/whisperX

## 下一步（可选加强）

- 完整 E2E：在昇腾上下载 `facebook/wav2vec2-base-960h` + 跑 forced alignment（需确认 faster-whisper/ctranslate2 的 aarch64 可用性、transformers Wav2Vec2 在 torch_npu 上的推理）。
- whisperX 其余依赖在 aarch64 的可用性（`torchvision~=0.23.0` 无昇腾对应 wheel、pyannote-audio 的 torchcodec 无 aarch64 wheel 等）是独立的第二个适配点。