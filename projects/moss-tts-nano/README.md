# MOSS-TTS-Nano（OpenMOSS）— ONNX 运行时去 torch 化

- 仓库: https://github.com/OpenMOSS/MOSS-TTS-Nano （4272★，非华为系）
- Issue: [#73](https://github.com/OpenMOSS/MOSS-TTS-Nano/issues/73) — README 宣称 ONNX 推理无 PyTorch 依赖，但 `onnx_tts_runtime.py` 顶层 `import torch/torchaudio`，无 torch 环境直接 ImportError
- PR: [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99)（2026-08-30 提交，分支 `torch-free-onnx-runtime`）
- 状态: IN_WINDOW（观察至 2026-09-06）

## 根因

ONNX 运行时唯一用 torch/torchaudio 的地方是 `_load_reference_audio()`（语音克隆参考音频加载/重采样/声道转换）。模块级 import 使整个 ONNX 部署路径在 ARM64/proot 等无 torch 环境崩掉。

## 修复（+72/-8，设备无关，无 if npu:）

- `torchaudio.load` → `soundfile.read(dtype="float32", always_2d=True)`（同 (channels,time) 布局与 [-1,1] 归一化，soundfile 已在 requirements.txt）
- `torchaudio.functional.resample` → 纯 NumPy 多相窗 sinc 重采样 `_resample_waveform()`（Hann 窗、每侧 32 taps，与 torchaudio 同插值族）
- `torch.Tensor.repeat/mean` → `np.repeat/np.mean`
- soundfile 改为可选 import，缺失时报清晰 ImportError

## 验证（177 容器 aarch64，无 torch/torchaudio 环境）

1. `import onnx_tts_runtime` 成功（修复前 ImportError）
2. 重采样 vs `scipy.signal.resample_poly`（同窗 sinc 族）：44100→24000 / 48000→16000 / 16000→24000 / 22050→16000 长度一致，中央区最大误差 < 8e-4
3. `_load_reference_audio` 端到端：mono 直通（幅值位精确）、立体声→单声道、44.1k→24k 重采样，输出 (1,1,N) float32
4. 同采样率恒等

## 备注

维护者月度批次合入（最近 merged 2026-07-26），非逐条 review 型社区。
