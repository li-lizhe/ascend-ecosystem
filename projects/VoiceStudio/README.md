# VoiceStudio (debpalash/VoiceStudio)

Ascend NPU 设备无关适配：把 TTS engine 里硬编码的 CUDA-or-CPU 设备选择改为
`torch.accelerator.current_accelerator()`，让 MOSS-TTS-v1.5 / Confucius4 /
DOTS-TTS 在昇腾 NPU 上自动跑 NPU + bf16，而不是静默退回 CPU + fp32。

- 仓库: https://github.com/debpalash/VoiceStudio (约 19k★)
- 活跃度: pushed<1d, 近 30 条 closed merge 率 100% —— 高活跃 live-review 社区

## 问题 / 根因

三个 TTS engine sidecar 都用 `torch.cuda.is_available()` 判设备：

- `moss_tts_v15/main.py`: `device = "cuda" if torch.cuda.is_available() else "cpu"`,
  `dtype = torch.bfloat16 if device == "cuda" else torch.float32`
- `confucius4/main.py`: `device = "cuda" if torch.cuda.is_available() else "cpu"`
- `dots_tts/main.py`: `default_precision = "bfloat16" if torch.cuda.is_available() else "float32"`

在昇腾 NPU（torch_npu）主机上 `torch.cuda.is_available()` 恒为 False → 模型静默跑 CPU + fp32，
完全用不上 NPU。同一 bug 波及 Intel XPU / AMD ROCm 等所有非 CUDA 加速器。

根因：`torch.cuda.is_available()` 是 CUDA 专属，不识别 npu/xpu/mps。设备无关的
正确 API 是 `torch.accelerator.current_accelerator()`（PyTorch Multi-Device 上游先例）。

## 修复

改用 `torch.accelerator.current_accelerator().type` 自动识别 CUDA/NPU/XPU/MPS/CPU：

- MPS 仍排除（MOSS/Confucius 上游 trust_remote_code 代码未在 Apple Silicon 测试）
- dtype：任意 GPU 类加速器用 bf16，CPU 用 fp32

## 验证（Ascend 910B, torch 2.14 + torch_npu, 4 卡）

```
torch.accelerator.current_accelerator().type == 'npu'   # 修复后
torch.cuda.is_available() == False                      # 旧代码的判定依据
```

- moss_tts_v15: 旧→device "cpu"/float32（错），新→device "npu"/bfloat16（对）
- confucius4: 旧→device "cpu"（错），新→device "npu"（对）
- dots_tts:   旧→precision "float32"（慢），新→"bfloat16"（快）

## PR

- https://github.com/debpalash/VoiceStudio/pull/1830 — `fix(moss_tts_v15): select device via torch.accelerator instead of CUDA hardcode`
- https://github.com/debpalash/VoiceStudio/pull/1831 — `fix(tts-engines): select device via torch.accelerator in confucius4 and dots_tts`

提交日期: 2026-09-06（早间新增）
