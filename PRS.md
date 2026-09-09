# 汇总 PR 清单

> 每项目详情见 `projects/<name>/README.md`。状态自动更新，更新频率：每日 09:00 + 21:00。

## ✅ 已合并（上游合入，10 个）

| 项目 | 变更 | PR | 合入日期 |
|------|------|----|---------|
| [FunASR](projects/funasr/) | 去 torchaudio 硬依赖（fbank → kaldi-native-fbank、音频加载 → soundfile、可选导入） | [#3526](https://github.com/modelscope/FunASR/pull/3526) | 2026-08-26 |
| [ComfyUI LayerStyle](projects/ComfyUI_LayerStyle/) | 设备无关映射（`torch.cuda` → `torch.accelerator`） | [#609](https://github.com/chflame163/ComfyUI_LayerStyle/pull/609) | 2026-09-03 |
| [VoiceStudio](projects/VoiceStudio/) | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1830](https://github.com/debpalash/VoiceStudio/pull/1830) | 2026-09-07 |
| [VoiceStudio](projects/VoiceStudio/) | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1831](https://github.com/debpalash/VoiceStudio/pull/1831) | 2026-09-07 |
| [kornia](projects/kornia/) | RT-DETR device-agnostic map_location | [#4212](https://github.com/kornia/kornia/pull/4212) | 2026-09-05 |
| [kornia](projects/kornia/) | Z1Projection.unproject 标量 depth 设备/dtype 继承 | [#4340](https://github.com/kornia/kornia/pull/4340) | 2026-09-07 |
| [snntorch](projects/snntorch/) | state_quant 保留输入 dtype | [#444](https://github.com/jeshraghian/snntorch/pull/444) | 2026-09-05 |
| [snntorch](projects/snntorch/) | spikegen.latency 保留输入 dtype | [#445](https://github.com/jeshraghian/snntorch/pull/445) | 2026-09-05 |
| [snntorch](projects/snntorch/) | `utils.reset(net)` 作用域修复 | [#449](https://github.com/jeshraghian/snntorch/pull/449) | 2026-09-08 |
| [spikingjelly](projects/spikingjelly/) | DSpike surrogate 函数重构兼容（`__init__` 参数顺序错位） | [#748](https://github.com/fangwei123456/spikingjelly/pull/748) | 2026-09-06 |

## 📡 跟踪中（PR open / 待 review，18 个）

| 项目 | 变更 | PR | 状态 |
|------|------|----|------|
| [kornia](projects/kornia/) | bbox_to_mask3d 保留输入 dtype | [#4376](https://github.com/kornia/kornia/pull/4376) | open（等待 review） |
| [kornia](projects/kornia/) | Boxes 整数坐标按默认 dtype 转浮点 | [#4379](https://github.com/kornia/kornia/pull/4379) | open（新提交） |
| [kornia](projects/kornia/) | PinholeCamera.scale_ int64 height/width dtype 提升（原地版） | [#4371](https://github.com/kornia/kornia/pull/4371) | CHANGES_REQUESTED（待回复 @ducha-aiki） |
| [GPT-SoVITS](projects/gpt-sovits/) | 导出脚本 device 无关加速器检测 | [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) | 待 review |
| [chatterbox](projects/chatterbox/) | `from_local`/`from_pretrained` device 标准化 | [#554](https://github.com/resemble-ai/chatterbox/pull/554) | 待 review |
| [whisperX](projects/whisperX/) | torchaudio 可选化 + Hugging Face 兜底 | [#1469](https://github.com/m-bain/whisperX/pull/1469) | 待 review |
| [ai-toolkit](projects/ai-toolkit/) | torchaudio 可选化 + captioner librosa 兜底 | [#1022](https://github.com/ostris/ai-toolkit/pull/1022) | 待 review |
| [docling](projects/docling/) | transformer engine 输入 dtype 与模型权重对齐 | [#4158](https://github.com/docling-project/docling/pull/4158) | 待 review |
| [speechbrain](projects/speechbrain/) | 设备无关适配 | [#3080](https://github.com/speechbrain/speechbrain/pull/3080) | 待 review |
| [ComfyUI-KJNodes](projects/comfyui-kjnodes/) | 设备无关 dtype 修复 | [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749) | 待 review |
| [musubi-tuner](projects/musubi-tuner/) | fp8_scaled 非 scaled_mm 路径 dtype mismatch | [#1079](https://github.com/kohya-ss/musubi-tuner/pull/1079) | 待 review |
| [LightX2V](projects/LightX2V/) | 设备无关 dtype 修复 | [#1470](https://github.com/ModelTC/LightX2V/pull/1470) | 待 review |
| [FastVideo](projects/FastVideo/) | device_map 设备无关 + autocast 修复（2 PR） | [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) · [#1818](https://github.com/hao-ai-lab/FastVideo/pull/1818) | 待 review |
| [MOSS-TTS-Nano](projects/moss-tts-nano/) | 设备无关适配 | [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99) | 待 review |
| [ebook2audiobook](projects/ebook2audiobook/) | 设备无关适配 | [#2071](https://github.com/DrewThomasson/ebook2audiobook/pull/2071) | 待 review |
| langgenius/dify | monaco worker 设备无关适配 | [#39341](https://github.com/langgenius/dify/pull/39341) | 待 review |
| [OpenADMET](projects/openadmet/) | TabPFN 模型类 accelerator→device 映射修复 | [#601](https://github.com/OpenADMET/openadmet-models/pull/601) | open（新提交） |