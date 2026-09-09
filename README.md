# Ascend Ecosystem · 昇腾生态适配

在国产昇腾（Ascend）NPU 上，让优秀的开源软件**开箱即用**，并把适配改动以**设备无关、最小侵入**的方式提交回上游，形成可复现、可推广的技术内容。

## 目标

三个坚持：

1. **设备无关** —— 不写 `if npu:` 硬件特判，统一走 PyTorch 多设备抽象（`torch.accelerator` / `device_type`）。
2. **最小侵入** —— 保留原后端优先路径，只在目标平台不可用时兜底，x86 用户零影响。
3. **先验证后提交** —— 所有改动在真实 910B 环境跑通 E2E 再提 PR，附性能 / 精度数据。

## 已完成项目

| 项目 | 内容 | 状态 | 上游 PR |
|------|------|------|---------|
| [FunASR](projects/funasr/) | 去 torchaudio 硬依赖（fbank → kaldi-native-fbank、音频加载 → soundfile、可选导入） | ✅ **已合并** | [#3526](https://github.com/modelscope/FunASR/pull/3526) |
| [ComfyUI LayerStyle](projects/ComfyUI_LayerStyle/) | 设备无关映射（`torch.cuda` → `torch.accelerator`） | ✅ **已合并** | [#609](https://github.com/chflame163/ComfyUI_LayerStyle/pull/609) |
| [VoiceStudio](projects/VoiceStudio/) | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA 判定） | ✅ **已合并** | [#1830](https://github.com/debpalash/VoiceStudio/pull/1830) · [#1831](https://github.com/debpalash/VoiceStudio/pull/1831) |
| [kornia](projects/kornia/) | 6 个设备无关/dtype 修复（RT-DETR map_location、Z1Projection 标量 depth、scale_ dtype、rad2deg/deg2rad 精度、bbox_to_mask3d dtype、Boxes 默认 dtype） | 5 合并 / 1 open | 详见 [projects/kornia/](projects/kornia/) |
| [snntorch](projects/snntorch/) | dtype 保持系列（state_quant / latency / reset 作用域） | ✅ **已合并** | [#444](https://github.com/jeshraghian/snntorch/pull/444) · [#445](https://github.com/jeshraghian/snntorch/pull/445) · [#449](https://github.com/jeshraghian/snntorch/pull/449) |
| [spikingjelly](projects/spikingjelly/) | DSpike surrogate 函数重构兼容（`__init__` 参数顺序错位） | ✅ **已合并** | [#748](https://github.com/fangwei123456/spikingjelly/pull/748) |
| [GPT-SoVITS](projects/gpt-sovits/) | 导出脚本 device 无关加速器检测（NPU/XPU/MPS） | PR 待 review | [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) |
| [chatterbox](projects/chatterbox/) | `from_local`/`from_pretrained` device 标准化（`torch.device` vs str 比较 bug） | PR 待 review | [#554](https://github.com/resemble-ai/chatterbox/pull/554) |
| [whisperX](projects/whisperX/) | torchaudio 可选化 + Hugging Face 兜底 | PR 待 review | [#1469](https://github.com/m-bain/whisperX/pull/1469) |
| [ai-toolkit](projects/ai-toolkit/) | torchaudio 可选化 + captioner librosa 兜底 | PR 待 review | [#1022](https://github.com/ostris/ai-toolkit/pull/1022) |
| [docling](projects/docling/) | transformer engine 输入 dtype 与模型权重对齐 | PR 待 review | [#4158](https://github.com/docling-project/docling/pull/4158) |
| [speechbrain](projects/speechbrain/) | 设备无关适配 | PR 待 review | [#3080](https://github.com/speechbrain/speechbrain/pull/3080) |
| [ComfyUI-KJNodes](projects/comfyui-kjnodes/) | 设备无关 dtype 修复 | PR 待 review | [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749) |
| [musubi-tuner](projects/musubi-tuner/) | fp8_scaled 非 scaled_mm 路径 dtype mismatch | PR 待 review | [#1079](https://github.com/kohya-ss/musubi-tuner/pull/1079) |
| [LightX2V](projects/LightX2V/) | 设备无关 dtype 修复 | PR 待 review | [#1470](https://github.com/ModelTC/LightX2V/pull/1470) |
| [FastVideo](projects/FastVideo/) | device_map 设备无关 + autocast 修复（2 PR） | PR 待 review | [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) · [#1818](https://github.com/hao-ai-lab/FastVideo/pull/1818) |
| [MOSS-TTS-Nano](projects/moss-tts-nano/) | 设备无关适配 | PR 待 review | [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99) |
| [ebook2audiobook](projects/ebook2audiobook/) | 设备无关适配 | PR 待 review | [#2071](https://github.com/DrewThomasson/ebook2audiobook/pull/2071) |
| [OpenADMET](projects/openadmet/) | TabPFN 模型类 accelerator→device 映射修复 | PR 待 review | [#601](https://github.com/OpenADMET/openadmet-models/pull/601) |

## 规划中

见 **[roadmap.md](roadmap.md)** —— 候选项目将逐一评估 → 适配 → 验证 → 提 PR → 写教程。

## 目录

```
tutorials/   推广教程（带截图，同步发知乎 / CSDN）
projects/    已完成项目的技术摘要与 PR 追踪
shared/      可复用件：去 torchaudio 化模板、checklist
roadmap.md   后续规划
```

## 环境

8× 昇腾 910B2（鲲鹏 ARM aarch64 · openEuler），torch `2.14.0a0`（华为 fork）+ torch_npu `2.14.0` + CANN 9.1。

## 参与

欢迎 issue / PR 提名想适配的项目，或 review 现有 PR。