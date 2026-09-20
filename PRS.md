# 汇总 PR 清单

> 每项目详情见 `projects/<name>/README.md`。状态由 GitHub API 核实（截至 2026-09-20）。
> 已合入 22 · 跟踪中 46 · 关闭未合入 10（见 EXCLUDED.md）。其中 **8 个需处理**（见 🔴 需处理区块）。

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

## 🔴 需处理（维护者有要求 / 未解决，2026-09-20）

> 以下 PR 有真实维护者 review 或评论需要跟进，优先处理。

| 项目 | PR | 问题 | 需做什么 |
|------|----|------|---------|
| [kornia](projects/kornia/) | [#4624](https://github.com/kornia/kornia/pull/4624) | CHANGES_REQUESTED（多轮，最新 09-17） | 修 `LightGlue.forward`（`lightglue.py:693`）用嵌套字典第一个 tensor 的 device 选 autocast 后端的问题（依赖字典顺序、会选错后端），并补 CPU 回归测试证明不破坏 CPU/MPS |
| [kornia](projects/kornia/) | [#4371](https://github.com/kornia/kornia/pull/4371) | CHANGES_REQUESTED（最新 09-17） | 测试期望张量用 `float64` 但乘法提升为 `float32`，导致全部 float64 CI leg 失败；从 `cam.height/width` 构造期望值而非 intrinsics fixture dtype |
| [FunASR](projects/funasr/) | [#3710](https://github.com/modelscope/FunASR/pull/3710) | CHANGES_REQUESTED（09-15） | 测试两个启动问题（`compute_var` 是静态方法非模块级导出；`f32_worker` 定义在方法内用 spawn 会 `Can't pickle local object`）；Manager/子进程加 `try/finally`（`join(timeout=60)` 不终止 worker） |
| [docling](projects/docling/) | [#4158](https://github.com/docling-project/docling/pull/4158) | 维护者给了具体改法，未跟进（09-07） | 用内置 `.to(self._device, self._model.dtype)` 替代手写 cast（`BatchFeature.to()` 第二参数只 cast 浮点，整数保持 dtype） |
| [lmdeploy](projects/lmdeploy/) | [#4986](https://github.com/InternLM/lmdeploy/pull/4986) | 有维护者评论要回应（09-18） | `pos_freq_scaling.to(seq_len.device)` 每次 forward 拷贝 CPU→设备，decode 有性能回归；像 `inv_freq` 一样缓存迁移后的 tensor |
| [peft](projects/peft/) | [#3734](https://github.com/huggingface/peft/pull/3734) | 有维护者质疑，需回应（09-17） | `ephemeral_gpu_offload=True` 语义是让 LoRA 临时上 GPU，直接用 base model device 可能违背该选项目的——回复解释或调整 |
| [peft](projects/peft/) | [#3766](https://github.com/huggingface/peft/pull/3766) | 可能撞车（09-19） | 维护者 `eSVeeF` 说与 issue #3753 同 bug，且有意开 PR——考虑在 PR 里关联 issue，避免被抢 |
| [PaddleOCR](projects/paddleocr/) | [#18370](https://github.com/PaddlePaddle/PaddleOCR/pull/18370) | **CLA 未签** | 去 [cla-assistant](https://cla-assistant.io/PaddlePaddle/PaddleOCR?pullRequest=18370) 签署 CLA 才能合入 |

## 📡 跟踪中（PR open / 待 review，46 个）

| 项目 | 变更 | PR | 提交时间 | 状态 |
|------|------|----|---------|------|
| [kornia](projects/kornia/) | PinholeCamera.scale_ int64 height/width dtype 提升 | [#4371](https://github.com/kornia/kornia/pull/4371) | 2026-09-08 | 🔴 待处理（见上方） |
| [kornia](projects/kornia/) | lightglue AMP device_type 通过 accelerator 解析 | [#4624](https://github.com/kornia/kornia/pull/4624) | 2026-09-17 | 🔴 待处理（见上方） |
| [GPT-SoVITS](projects/gpt-sovits/) | 导出脚本 device 无关加速器检测 | [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) | 2026-09-04 | open（待 review） |
| [chatterbox](projects/chatterbox/) | `from_local`/`from_pretrained` device 标准化 | [#554](https://github.com/resemble-ai/chatterbox/pull/554) | 2026-08-27 | open（待 review） |
| [whisperX](projects/whisperX/) | torchaudio 可选化 + Hugging Face 兜底 | [#1469](https://github.com/m-bain/whisperX/pull/1469) | 2026-08-27 | open（待 review） |
| [ai-toolkit](projects/ai-toolkit/) | torchaudio 可选化 + captioner librosa 兜底 | [#1022](https://github.com/ostris/ai-toolkit/pull/1022) | 2026-08-29 | open（待 review） |
| [docling](projects/docling/) | transformer engine 输入 dtype 与模型权重对齐 | [#4158](https://github.com/docling-project/docling/pull/4158) | 2026-09-04 | 🔴 待处理（见上方） |
| [speechbrain](projects/speechbrain/) | infer_device 用 torch.accelerator 支持非 CUDA | [#3080](https://github.com/speechbrain/speechbrain/pull/3080) | 2026-09-02 | open（待 review） |
| [speechbrain](projects/speechbrain/) | weight_norm parametrizations 静默 deprecation 警告 | [#3087](https://github.com/speechbrain/speechbrain/pull/3087) | 2026-09-19 | open（待 review） |
| [ComfyUI-KJNodes](projects/comfyui-kjnodes/) | WanVideoNAG dtype mismatch 修复 | [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749) | 2026-09-02 | open（待 review） |
| [musubi-tuner](projects/musubi-tuner/) | fp8_scaled 非 scaled_mm 路径 dtype mismatch | [#1079](https://github.com/kohya-ss/musubi-tuner/pull/1079) | 2026-08-31 | open（待 review） |
| [LightX2V](projects/LightX2V/) | pre-weights 忽略 dit_quant_scheme（fp8 dtype） | [#1470](https://github.com/ModelTC/LightX2V/pull/1470) | 2026-09-01 | open（待 review） |
| [FastVideo](projects/FastVideo/) | SceneMetric device_map 设备无关 | [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) | 2026-09-05 | open（待 review） |
| [MOSS-TTS-Nano](projects/moss-tts-nano/) | ONNX runtime 路径 torch-free | [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99) | 2026-08-30 | open（待 review） |
| langgenius/dify | MonacoEnvironment.getWorkerUrl 设备无关 | [#39341](https://github.com/langgenius/dify/pull/39341) | 2026-07-21 | open（待 review） |
| [OpenADMET](projects/openadmet/) | 'auto' accelerator（非 'gpu'）作默认 | [#604](https://github.com/OpenADMET/openadmet-models/pull/604) | 2026-09-18 | open（待 review） |
| [FunASR](projects/funasr/) | y.device 替代硬编码 .cuda() | [#3710](https://github.com/modelscope/FunASR/pull/3710) | 2026-09-15 | 🔴 待处理（见上方） |
| openai/whisper | torch.accelerator 默认设备选择 | [#2855](https://github.com/openai/whisper/pull/2855) | 2026-09-12 | open（待 review） |
| [unsloth](projects/unsloth/) | LlamaFactory 梯度切分/设备回退 | [LlamaFactory #10828](https://github.com/hiyouga/LlamaFactory/pull/10828) | 2026-09-10 | open（待 review） |
| [unsloth](projects/unsloth/) | longlora device type 检查扩展 | [LlamaFactory #10829](https://github.com/hiyouga/LlamaFactory/pull/10829) | 2026-09-10 | open（待 review） |
| [axolotl](projects/axolotl/) | 梯度 checkpointing offload 设备无关 | [#3995](https://github.com/axolotl-ai-cloud/axolotl/pull/3995) | 2026-09-11 | open（待 review） |
| [axolotl](projects/axolotl/) | AMP custom_fwd/bwd 设备无关 | [#3996](https://github.com/axolotl-ai-cloud/axolotl/pull/3996) | 2026-09-11 | open（待 review） |
| [DeepSpeed](projects/deepspeed/) | zenflow 用 optimizer_z3.device | [#8524](https://github.com/deepspeedai/DeepSpeed/pull/8524) | 2026-09-15 | open（待 review） |
| [DeepSpeed](projects/deepspeed/) | data_pipeline 默认 active accelerator | [#8525](https://github.com/deepspeedai/DeepSpeed/pull/8525) | 2026-09-15 | open（待 review） |
| [diffusers](projects/diffusers/) | wan 设备无关默认值 | [#14765](https://github.com/huggingface/diffusers/pull/14765) | 2026-09-14 | open（待 review） |
| [diffusers](projects/diffusers/) | minimax 全加速器 autocast | [#14766](https://github.com/huggingface/diffusers/pull/14766) | 2026-09-14 | open（待 review） |
| [diffusers](projects/diffusers/) | group_offloading 支持 Ascend NPU stream | [#14785](https://github.com/huggingface/diffusers/pull/14785) | 2026-09-16 | open（待 review） |
| [diffusers](projects/diffusers/) | modular_pipeline 含 Ascend NPU | [#14786](https://github.com/huggingface/diffusers/pull/14786) | 2026-09-16 | open（待 review） |
| [peft](projects/peft/) | dora 用 base layer device | [#3734](https://github.com/huggingface/peft/pull/3734) | 2026-09-13 | 🔴 待处理（见上方） |
| [peft](projects/peft/) | 新注入 layer 传播 training/eval 模式 | [#3766](https://github.com/huggingface/peft/pull/3766) | 2026-09-19 | 🔴 待处理（见上方） |
| [transformers](projects/transformers/) | ContinuousBatching 支持 NPU/XPU compute stream | [#48937](https://github.com/huggingface/transformers/pull/48937) | 2026-09-18 | open（待 review） |
| [lerobot](projects/lerobot/) | embedder 设备无关默认值 | [#4676](https://github.com/huggingface/lerobot/pull/4676) | 2026-09-18 | open（待 review） |
| [lerobot](projects/lerobot/) | fastwam Wan VAE 设备无关默认值 | [#4677](https://github.com/huggingface/lerobot/pull/4677) | 2026-09-18 | open（待 review） |
| [lerobot](projects/lerobot/) | device type 比较含 npu/xpu | [#4678](https://github.com/huggingface/lerobot/pull/4678) | 2026-09-18 | open（待 review） |
| [datasets](projects/datasets/) | py_utils 保存/恢复 NPU RNG state | [#8644](https://github.com/huggingface/datasets/pull/8644) | 2026-09-18 | open（待 review） |
| [lmdeploy](projects/lmdeploy/) | dlinfer NTK rotary 移除 CUDA 硬编码 | [#4986](https://github.com/InternLM/lmdeploy/pull/4986) | 2026-09-18 | 🔴 待处理（见上方） |
| [PaddleOCR](projects/paddleocr/) | parseq_head 移除冗余 cpu/cuda 往返 | [#18370](https://github.com/PaddlePaddle/PaddleOCR/pull/18370) | 2026-09-18 | 🔴 待处理（见上方） |
| [Megatron-LM](projects/megatron-lm/) | torch.amp.custom_fwd 动态 device_type | [#7422](https://github.com/NVIDIA/Megatron-LM/pull/7422) | 2026-09-17 | open（待 review） |
| [sdnext](projects/sdnext/) | autoencoder_kl 用 x.device | [#5098](https://github.com/vladmandic/sdnext/pull/5098) | 2026-09-19 | open（待 review） |
| [ComfyUI](projects/comfyui/) | pixart 用输入 tensor device 做 label | [#16331](https://github.com/Comfy-Org/ComfyUI/pull/16331) | 2026-09-15 | open（待 review） |
| [crewAI](projects/crewai/) | crewai-tools strip UTF-8 BOM | [#7602](https://github.com/crewAIInc/crewAI/pull/7602) | 2026-09-19 | open（待 review） |
| [crewAI](projects/crewai/) | evaluation 返回 False 替代 True | [#7603](https://github.com/crewAIInc/crewAI/pull/7603) | 2026-09-19 | open（待 review） |
| [sglang](projects/sglang/) | frozen-kv-mtp 接受 pp_proxy_tensors | [#40355](https://github.com/sgl-project/sglang/pull/40355) | 2026-09-19 | open（待 review） |
| [pytorch-lightning](projects/pytorch-lightning/) | sampler epoch 在迭代器创建前设置 | [#21960](https://github.com/Lightning-AI/pytorch-lightning/pull/21960) | 2026-09-19 | open（待 review） |
| [torchmetrics](projects/torchmetrics/) | V-measure 独立聚类返回 0.0 非 1.0 | [#3506](https://github.com/Lightning-AI/torchmetrics/pull/3506) | 2026-09-19 | open（待 review） |
| [torchmetrics](projects/torchmetrics/) | forward 保留累计 metric state | [#3507](https://github.com/Lightning-AI/torchmetrics/pull/3507) | 2026-09-19 | open（待 review） |
