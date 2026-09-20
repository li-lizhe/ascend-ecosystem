# 汇总 PR 清单

> 每项目详情见 `projects/<name>/README.md`。状态由 GitHub API 核实（截至 2026-09-20）。
> 已合入 22 · 跟踪中 46 · 关闭未合入 10（见 EXCLUDED.md）。

## ✅ 已合并（上游合入，22 个）

| 项目 | 变更 | PR | 合入日期 |
|------|------|----|---------|
| [FunASR](projects/funasr/) | 去 torchaudio 硬依赖（fbank → kaldi-native-fbank、音频加载 → soundfile、可选导入） | [#3526](https://github.com/modelscope/FunASR/pull/3526) | 2026-08-26 |
| [ComfyUI LayerStyle](projects/ComfyUI_LayerStyle/) | 设备无关映射（`torch.cuda` → `torch.accelerator`） | [#609](https://github.com/chflame163/ComfyUI_LayerStyle/pull/609) | 2026-09-03 |
| [snntorch](projects/snntorch/) | state_quant 保留输入 dtype | [#444](https://github.com/jeshraghian/snntorch/pull/444) | 2026-09-05 |
| [snntorch](projects/snntorch/) | spikegen.latency 保留输入 dtype | [#445](https://github.com/jeshraghian/snntorch/pull/445) | 2026-09-05 |
| [kornia](projects/kornia/) | RT-DETR device-agnostic map_location | [#4212](https://github.com/kornia/kornia/pull/4212) | 2026-09-05 |
| [spikingjelly](projects/spikingjelly/) | DSpike surrogate 函数重构兼容（`__init__` 参数顺序错位） | [#748](https://github.com/fangwei123456/spikingjelly/pull/748) | 2026-09-06 |
| [VoiceStudio](projects/VoiceStudio/) | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1830](https://github.com/debpalash/VoiceStudio/pull/1830) | 2026-09-07 |
| [VoiceStudio](projects/VoiceStudio/) | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1831](https://github.com/debpalash/VoiceStudio/pull/1831) | 2026-09-07 |
| [kornia](projects/kornia/) | Z1Projection.unproject 标量 depth 设备/dtype 继承 | [#4340](https://github.com/kornia/kornia/pull/4340) | 2026-09-07 |
| [snntorch](projects/snntorch/) | `utils.reset(net)` 作用域修复 | [#449](https://github.com/jeshraghian/snntorch/pull/449) | 2026-09-08 |
| [OpenADMET](projects/openadmet/) | TabPFN 模型类 accelerator→device 映射修复 | [#601](https://github.com/OpenADMET/openadmet-models/pull/601) | 2026-09-10 |
| [sdnext](projects/sdnext/) | framepack 用 text_mask.device 替代硬编码 | [#5085](https://github.com/vladmandic/sdnext/pull/5085) | 2026-09-12 |
| [kornia](projects/kornia/) | bbox_to_mask3d 保留输入 dtype | [#4376](https://github.com/kornia/kornia/pull/4376) | 2026-09-13 |
| [snntorch](projects/snntorch/) | population-code helpers 保留输入 dtype（#428 #429） | [#451](https://github.com/jeshraghian/snntorch/pull/451) | 2026-09-14 |
| [unsloth](projects/unsloth/) | chat_templates 移除 CUDA 硬编码设备 | [#10684](https://github.com/unslothai/unsloth/pull/10684) | 2026-09-14 |
| [unsloth](projects/unsloth/) | device_type 增加 Ascend NPU 检测 | [#10686](https://github.com/unslothai/unsloth/pull/10686) | 2026-09-14 |
| [unsloth](projects/unsloth/) | sentence_transformer 设备一致性 | [#10843](https://github.com/unslothai/unsloth/pull/10843) | 2026-09-14 |
| [kornia](projects/kornia/) | Boxes 整数坐标按默认 dtype 转浮点 | [#4379](https://github.com/kornia/kornia/pull/4379) | 2026-09-15 |
| [FastVideo](projects/FastVideo/) | AdaLayerNorm autocast 设备无关 | [#1818](https://github.com/hao-ai-lab/FastVideo/pull/1818) | 2026-09-15 |
| [ComfyUI LayerStyle](projects/ComfyUI_LayerStyle/) | 硬编码 CUDA 节点加 'auto' 设备选项 | [#610](https://github.com/chflame163/ComfyUI_LayerStyle/pull/610) | 2026-09-16 |
| [spikingjelly](projects/spikingjelly/) | `_resolve_device_type` 返回实际 device type | [#755](https://github.com/fangwei123456/spikingjelly/pull/755) | 2026-09-18 |
| [VoiceStudio](projects/VoiceStudio/) | model_manager 增加 Ascend NPU 支持 | [#2194](https://github.com/debpalash/VoiceStudio/pull/2194) | 2026-09-18 |

## 📡 跟踪中（PR open / 待 review，46 个）

| 项目 | 变更 | PR | 状态 |
|------|------|----|------|
| [kornia](projects/kornia/) | PinholeCamera.scale_ int64 height/width dtype 提升 | [#4371](https://github.com/kornia/kornia/pull/4371) | open（待 review） |
| [kornia](projects/kornia/) | lightglue AMP device_type 通过 accelerator 解析 | [#4624](https://github.com/kornia/kornia/pull/4624) | open（待 review） |
| [GPT-SoVITS](projects/gpt-sovits/) | 导出脚本 device 无关加速器检测 | [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) | open（待 review） |
| [chatterbox](projects/chatterbox/) | `from_local`/`from_pretrained` device 标准化 | [#554](https://github.com/resemble-ai/chatterbox/pull/554) | open（待 review） |
| [whisperX](projects/whisperX/) | torchaudio 可选化 + Hugging Face 兜底 | [#1469](https://github.com/m-bain/whisperX/pull/1469) | open（待 review） |
| [ai-toolkit](projects/ai-toolkit/) | torchaudio 可选化 + captioner librosa 兜底 | [#1022](https://github.com/ostris/ai-toolkit/pull/1022) | open（待 review） |
| [docling](projects/docling/) | transformer engine 输入 dtype 与模型权重对齐 | [#4158](https://github.com/docling-project/docling/pull/4158) | open（待 review） |
| [speechbrain](projects/speechbrain/) | infer_device 用 torch.accelerator 支持非 CUDA | [#3080](https://github.com/speechbrain/speechbrain/pull/3080) | open（待 review） |
| [speechbrain](projects/speechbrain/) | weight_norm parametrizations 静默 deprecation 警告 | [#3087](https://github.com/speechbrain/speechbrain/pull/3087) | open（待 review） |
| [ComfyUI-KJNodes](projects/comfyui-kjnodes/) | WanVideoNAG dtype mismatch 修复 | [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749) | open（待 review） |
| [musubi-tuner](projects/musubi-tuner/) | fp8_scaled 非 scaled_mm 路径 dtype mismatch | [#1079](https://github.com/kohya-ss/musubi-tuner/pull/1079) | open（待 review） |
| [LightX2V](projects/LightX2V/) | pre-weights 忽略 dit_quant_scheme（fp8 dtype） | [#1470](https://github.com/ModelTC/LightX2V/pull/1470) | open（待 review） |
| [FastVideo](projects/FastVideo/) | SceneMetric device_map 设备无关 | [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) | open（待 review） |
| [MOSS-TTS-Nano](projects/moss-tts-nano/) | ONNX runtime 路径 torch-free | [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99) | open（待 review） |
| langgenius/dify | MonacoEnvironment.getWorkerUrl 设备无关 | [#39341](https://github.com/langgenius/dify/pull/39341) | open（待 review） |
| [OpenADMET](projects/openadmet/) | 'auto' accelerator（非 'gpu'）作默认 | [#604](https://github.com/OpenADMET/openadmet-models/pull/604) | open（待 review） |
| [FunASR](projects/funasr/) | y.device 替代硬编码 .cuda() | [#3710](https://github.com/modelscope/FunASR/pull/3710) | open（待 review） |
| openai/whisper | torch.accelerator 默认设备选择 | [#2855](https://github.com/openai/whisper/pull/2855) | open（待 review） |
| [unsloth](projects/unsloth/) | LlamaFactory 梯度切分/设备回退 | [LlamaFactory #10828](https://github.com/hiyouga/LlamaFactory/pull/10828) | open（待 review） |
| [unsloth](projects/unsloth/) | longlora device type 检查扩展 | [LlamaFactory #10829](https://github.com/hiyouga/LlamaFactory/pull/10829) | open（待 review） |
| [axolotl](projects/axolotl/) | 梯度 checkpointing offload 设备无关 | [#3995](https://github.com/axolotl-ai-cloud/axolotl/pull/3995) | open（待 review） |
| [axolotl](projects/axolotl/) | AMP custom_fwd/bwd 设备无关 | [#3996](https://github.com/axolotl-ai-cloud/axolotl/pull/3996) | open（待 review） |
| [DeepSpeed](projects/deepspeed/) | zenflow 用 optimizer_z3.device | [#8524](https://github.com/deepspeedai/DeepSpeed/pull/8524) | open（待 review） |
| [DeepSpeed](projects/deepspeed/) | data_pipeline 默认 active accelerator | [#8525](https://github.com/deepspeedai/DeepSpeed/pull/8525) | open（待 review） |
| [diffusers](projects/diffusers/) | wan 设备无关默认值 | [#14765](https://github.com/huggingface/diffusers/pull/14765) | open（待 review） |
| [diffusers](projects/diffusers/) | minimax 全加速器 autocast | [#14766](https://github.com/huggingface/diffusers/pull/14766) | open（待 review） |
| [diffusers](projects/diffusers/) | group_offloading 支持 Ascend NPU stream | [#14785](https://github.com/huggingface/diffusers/pull/14785) | open（待 review） |
| [diffusers](projects/diffusers/) | modular_pipeline 含 Ascend NPU | [#14786](https://github.com/huggingface/diffusers/pull/14786) | open（待 review） |
| [peft](projects/peft/) | dora 用 base layer device | [#3734](https://github.com/huggingface/peft/pull/3734) | open（待 review） |
| [peft](projects/peft/) | 新注入 layer 传播 training/eval 模式 | [#3766](https://github.com/huggingface/peft/pull/3766) | open（待 review） |
| [transformers](projects/transformers/) | ContinuousBatching 支持 NPU/XPU compute stream | [#48937](https://github.com/huggingface/transformers/pull/48937) | open（待 review） |
| [lerobot](projects/lerobot/) | embedder 设备无关默认值 | [#4676](https://github.com/huggingface/lerobot/pull/4676) | open（待 review） |
| [lerobot](projects/lerobot/) | fastwam Wan VAE 设备无关默认值 | [#4677](https://github.com/huggingface/lerobot/pull/4677) | open（待 review） |
| [lerobot](projects/lerobot/) | device type 比较含 npu/xpu | [#4678](https://github.com/huggingface/lerobot/pull/4678) | open（待 review） |
| [datasets](projects/datasets/) | py_utils 保存/恢复 NPU RNG state | [#8644](https://github.com/huggingface/datasets/pull/8644) | open（待 review） |
| [lmdeploy](projects/lmdeploy/) | dlinfer NTK rotary 移除 CUDA 硬编码 | [#4986](https://github.com/InternLM/lmdeploy/pull/4986) | open（待 review） |
| [PaddleOCR](projects/paddleocr/) | parseq_head 移除冗余 cpu/cuda 往返 | [#18370](https://github.com/PaddlePaddle/PaddleOCR/pull/18370) | open（待 review） |
| [Megatron-LM](projects/megatron-lm/) | torch.amp.custom_fwd 动态 device_type | [#7422](https://github.com/NVIDIA/Megatron-LM/pull/7422) | open（待 review） |
| [sdnext](projects/sdnext/) | autoencoder_kl 用 x.device | [#5098](https://github.com/vladmandic/sdnext/pull/5098) | open（待 review） |
| [ComfyUI](projects/comfyui/) | pixart 用输入 tensor device 做 label | [#16331](https://github.com/Comfy-Org/ComfyUI/pull/16331) | open（待 review） |
| [crewAI](projects/crewai/) | crewai-tools strip UTF-8 BOM | [#7602](https://github.com/crewAIInc/crewAI/pull/7602) | open（待 review） |
| [crewAI](projects/crewai/) | evaluation 返回 False 替代 True | [#7603](https://github.com/crewAIInc/crewAI/pull/7603) | open（待 review） |
| [sglang](projects/sglang/) | frozen-kv-mtp 接受 pp_proxy_tensors | [#40355](https://github.com/sgl-project/sglang/pull/40355) | open（待 review） |
| [pytorch-lightning](projects/pytorch-lightning/) | sampler epoch 在迭代器创建前设置 | [#21960](https://github.com/Lightning-AI/pytorch-lightning/pull/21960) | open（待 review） |
| [torchmetrics](projects/torchmetrics/) | V-measure 独立聚类返回 0.0 非 1.0 | [#3506](https://github.com/Lightning-AI/torchmetrics/pull/3506) | open（待 review） |
| [torchmetrics](projects/torchmetrics/) | forward 保留累计 metric state | [#3507](https://github.com/Lightning-AI/torchmetrics/pull/3507) | open（待 review） |
