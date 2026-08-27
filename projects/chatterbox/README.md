# Chatterbox · 昇腾 910B 适配

Resemble AI 的多语言 TTS 库 [chatterbox](https://github.com/resemble-ai/chatterbox)（约 2.6 万 star）—— 修复其 device 硬编码，打通 CPU/昇腾 NPU 等非 CUDA 加速器。

## 状态

🔧 第一步完成 · PR #554 已提交（device 无关修复）· 等待上游 review
下一步：去 torchaudio 硬依赖，让 chatterbox 完整跑通昇腾推理。

## 问题

`torch.device("cpu") in ["cpu", "mps"]` 为 `False`（`torch.device` 与 `str` 不相等），
导致 `from_local()` 的 `map_location=None`，在 CPU-only 机器反序列化 CUDA-saved
checkpoint 时报 `RuntimeError: Attempting to deserialize object on a CUDA device ...`。
同一隐患影响所有非 CUDA 加速器（`"npu"`、`"xpu"` 等）。
关联上游 issue：#533。

## 方案 —— device 无关化

1. 新增共享 helper `load_map_location(device)`：`torch.device(device)` 归一化，仅 CUDA 返回 `None`，其余加速器先加载到 CPU 再 `.to(device)`
2. 四个入口（`mtl_tts.py` / `tts.py` / `tts_turbo.py` / `vc.py`）替换重复的字符串比较逻辑
3. `from_pretrained()` 用 `device.type == "mps"` 判断 macOS MPS（同样的 `str` vs `torch.device` bug）

## 上游 PR

- **PR #554**：Fix device normalization in from_local/from_pretrained
  https://github.com/resemble-ai/chatterbox/pull/554 —— 5 文件 `+36/−24` + 1 测试
  Fork：https://github.com/li-lizhe/chatterbox

## 验证

- 8× 昇腾 910B2，torch `2.14.0a0+git69231fe`，torch_npu（4 卡）
- `load_map_location` 在 `cpu`/`mps`/`npu`/`xpu`/`cuda`/`cuda:0`（str 与 `torch.device` 两种入参）全分支正确
- 确认根因：`torch.device('cpu') in ['cpu','mps'] == False`（本 torch 构建）
- 回归测试 `tests/test_device_utils.py`

## 下一步（第二个 PR 的靶子）

chatterbox 硬 pin `torch==2.6.0` + `torchaudio==2.6.0`；昇腾 aarch64 + 华为 torch
(`2.14.0a0`) 无匹配 wheel，`import chatterbox` 即崩（`s3gen.py`/`xvector.py` 顶层
`import torchaudio`）。所需适配：
1. `torchaudio.transforms.Resample` → librosa/soundfile 兜底
2. `torchaudio.compliance.kaldi.fbank` → kaldi-native-fbank 兜底（复用 FunASR shim）
3. 松开 `torch`/`torchaudio` 版本 pin，允许昇腾 torch