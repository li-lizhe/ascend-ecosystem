# 汇总 PR 清单（全景 · A/B 分账）

> 数据源：GitHub API 全量 `author:li-lizhe type:pr`，由 `prs_build.py` 重建 · 生成于 2026-09-27 01:11
>
> 括号内为**较前一次记录的变化量**。
>
> | 类别 | 范围 | 提交 | ✅ 已合入 | 📡 跟踪中 | ❌ 关闭未合入 | 处置权限 |
> |------|------|------|---------|---------|------------|---------|
> | 🅰️ **A 类** | pytorch 上游（`pytorch/*`、`li-lizhe/pytorch`） | 16 (±0) | 1 (-1) | 13 (±0) | 2 (+1) | **只报不动**：回复/改码/push 须用户审视确认 |
> | 🅱️ **B 类** | 昇腾生态 / 社区（其余全部） | 109 (+4) | 37 (+1) | 48 (±0) | 24 (+3) | 可自主：读 review→改码→测试→真机验证→回复/再提交 |
> | **合计** | | 125 (+4) | 38 (±0) | 61 (±0) | 26 (+4) | |
>
> **较昨日（基线 2026-09-26）：提交 +4 · ✅ 已合入 ±0 · 📡 跟踪中 ±0 · ❌ 关闭未合入 +4**
>
> 每日 06:00 的「昇腾PR邮件哨兵」以本表为活跃名单唯一权威源（脚本不再硬编码 PR 号）；关闭/合入即出栈归档。
> 说明：pytorch 的 bot merge 会让 API `merged` 恒为 False，本表已按 `Merged` label + closed commit 是否 main 祖先修正。

# 🅰️ A 类 · PyTorch 上游（只报不动，任何回复/改码须用户审视确认）

## 📡 A 类跟踪中（13）

| 项目 | 变更 | PR | 提交日期 |
|------|------|----|---------|
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_tp_integration.py to capabil… | [#192208](https://github.com/pytorch/pytorch/pull/192208) | 2026-08-05 |
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_comm to capability gating | [#192701](https://github.com/pytorch/pytorch/pull/192701) | 2026-08-10 |
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_dtensor_state_dict to capabi… | [#192700](https://github.com/pytorch/pytorch/pull/192700) | 2026-08-10 |
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_exec_order to capability gat… | [#192699](https://github.com/pytorch/pytorch/pull/192699) | 2026-08-10 |
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_flatten_params to capability… | [#192697](https://github.com/pytorch/pytorch/pull/192697) | 2026-08-10 |
| pytorch/pytorch | [Testcase Refactoring] Migrate test_fsdp_fine_tune to capability gati… | [#192696](https://github.com/pytorch/pytorch/pull/192696) | 2026-08-10 |
| li-lizhe/pytorch | [Testcase Refactoring] Add NPU/PrivateUse1 support to common_fsdp.py | [#1](https://github.com/li-lizhe/pytorch/pull/1) | 2026-08-13 |
| pytorch/pytorch | [Feature Refactoring] Route non-cpu RNG states from the accelerator s… | [#195261](https://github.com/pytorch/pytorch/pull/195261) | 2026-08-29 |
| pytorch/pytorch | [Feature Refactoring] Resolve fake process group supported devices la… | [#195260](https://github.com/pytorch/pytorch/pull/195260) | 2026-08-29 |
| pytorch/pytorch | [Feature Refactoring] Fall back to full-state RNG sync check for non-… | [#195248](https://github.com/pytorch/pytorch/pull/195248) | 2026-08-29 |
| pytorch/pytorch | [Feature Refactoring] Generalize RemoteModule device handling beyond … | [#195247](https://github.com/pytorch/pytorch/pull/195247) | 2026-08-29 |
| pytorch/pytorch | [Feature Refactoring] Consume registered RNG trackers in DTensor rand… | [#195246](https://github.com/pytorch/pytorch/pull/195246) | 2026-08-29 |
| pytorch/pytorch | [Feature Refactoring] Add register_rng_tracker API for device-specifi… | [#195245](https://github.com/pytorch/pytorch/pull/195245) | 2026-08-29 |

## ✅ A 类已合入（1）

| 项目 | 变更 | PR | 合入日期 |
|------|------|----|---------|
| pytorch/pytorch | [Testcase Refactoring] Generalize requires_world_size to … | [#192694](https://github.com/pytorch/pytorch/pull/192694) | 2026-09-21 |

## ❌ A 类关闭未合入（2）

| 项目 | 变更 | PR | 关闭日期 |
|------|------|----|---------|
| pytorch/pytorch | [Testcase Refactoring] Add NPU/PrivateUse1 support to common_fsdp.py | [#193347](https://github.com/pytorch/pytorch/pull/193347) | 2026-08-13 |
| pytorch/pytorch | [Testcase Refactoring] Demote test_fsdp_fx to Strategy 1 … | [#192698](https://github.com/pytorch/pytorch/pull/192698) | 2026-09-14 |

逐条留档见 `EXCLUDED.md`。

# 🅱️ B 类 · 昇腾生态 / 社区（可自主处置）

## 📡 B 类跟踪中（48）

| 项目 | 变更 | PR | 提交日期 |
|------|------|----|---------|
| langgenius/dify | MonacoEnvironment.getWorkerUrl 设备无关 | [#39341](https://github.com/langgenius/dify/pull/39341) | 2026-07-21 |
| m-bain/whisperX | torchaudio 可选化 + Hugging Face 兜底 | [#1469](https://github.com/m-bain/whisperX/pull/1469) | 2026-08-27 |
| resemble-ai/chatterbox | `from_local`/`from_pretrained` device 标准化 | [#554](https://github.com/resemble-ai/chatterbox/pull/554) | 2026-08-27 |
| ostris/ai-toolkit | torchaudio 可选化 + captioner librosa 兜底 | [#1022](https://github.com/ostris/ai-toolkit/pull/1022) | 2026-08-29 |
| OpenMOSS/MOSS-TTS-Nano | ONNX runtime 路径 torch-free | [#99](https://github.com/OpenMOSS/MOSS-TTS-Nano/pull/99) | 2026-08-30 |
| kohya-ss/musubi-tuner | fp8_scaled 非 scaled_mm 路径 dtype mismatch | [#1079](https://github.com/kohya-ss/musubi-tuner/pull/1079) | 2026-08-31 |
| ModelTC/LightX2V | pre-weights 忽略 dit_quant_scheme（fp8 dtype） | [#1470](https://github.com/ModelTC/LightX2V/pull/1470) | 2026-09-01 |
| speechbrain/speechbrain | infer_device 用 torch.accelerator 支持非 CUDA | [#3080](https://github.com/speechbrain/speechbrain/pull/3080) | 2026-09-02 |
| kijai/ComfyUI-KJNodes | WanVideoNAG dtype mismatch 修复 | [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749) | 2026-09-02 |
| RVC-Boss/GPT-SoVITS | 导出脚本 device 无关加速器检测 | [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) | 2026-09-04 |
| docling-project/docling | #4158 | [#4158](https://github.com/docling-project/docling/pull/4158) | 2026-09-04 |
| hao-ai-lab/FastVideo | SceneMetric device_map 设备无关 | [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) | 2026-09-05 |
| hiyouga/LlamaFactory | longlora device type 检查扩展 | [#10829](https://github.com/hiyouga/LlamaFactory/pull/10829) | 2026-09-10 |
| hiyouga/LlamaFactory | LlamaFactory 梯度切分/设备回退 | [#10828](https://github.com/hiyouga/LlamaFactory/pull/10828) | 2026-09-10 |
| axolotl-ai-cloud/axolotl | offload + AMP kernels 设备无关（合并#3996） | [#3995](https://github.com/axolotl-ai-cloud/axolotl/pull/3995) | 2026-09-11 |
| openai/whisper | torch.accelerator 默认设备选择 | [#2855](https://github.com/openai/whisper/pull/2855) | 2026-09-12 |
| deepspeedai/DeepSpeed | data_pipeline 默认 active accelerator | [#8525](https://github.com/deepspeedai/DeepSpeed/pull/8525) | 2026-09-15 |
| deepspeedai/DeepSpeed | zenflow 用 optimizer_z3.device | [#8524](https://github.com/deepspeedai/DeepSpeed/pull/8524) | 2026-09-15 |
| Comfy-Org/ComfyUI | pixart 用输入 tensor device 做 label | [#16331](https://github.com/Comfy-Org/ComfyUI/pull/16331) | 2026-09-15 |
| huggingface/diffusers | modular_pipeline 含 Ascend NPU | [#14786](https://github.com/huggingface/diffusers/pull/14786) | 2026-09-16 |
| huggingface/diffusers | group_offloading 支持 Ascend NPU stream | [#14785](https://github.com/huggingface/diffusers/pull/14785) | 2026-09-16 |
| NVIDIA/Megatron-LM | torch.amp.custom_fwd 动态 device_type | [#7422](https://github.com/NVIDIA/Megatron-LM/pull/7422) | 2026-09-17 |
| huggingface/transformers | ContinuousBatching 支持 NPU/XPU compute stream | [#48937](https://github.com/huggingface/transformers/pull/48937) | 2026-09-18 |
| huggingface/lerobot | device type 比较含 npu/xpu | [#4678](https://github.com/huggingface/lerobot/pull/4678) | 2026-09-18 |
| huggingface/lerobot | fastwam Wan VAE 设备无关默认值 | [#4677](https://github.com/huggingface/lerobot/pull/4677) | 2026-09-18 |
| OpenADMET/openadmet-models | 'auto' accelerator（非 'gpu'）作默认 | [#604](https://github.com/OpenADMET/openadmet-models/pull/604) | 2026-09-18 |
| huggingface/datasets | py_utils 保存/恢复 NPU RNG state | [#8644](https://github.com/huggingface/datasets/pull/8644) | 2026-09-18 |
| PaddlePaddle/PaddleOCR | #18370 | [#18370](https://github.com/PaddlePaddle/PaddleOCR/pull/18370) | 2026-09-18 |
| Lightning-AI/torchmetrics | forward 保留累计 metric state | [#3507](https://github.com/Lightning-AI/torchmetrics/pull/3507) | 2026-09-19 |
| sgl-project/sglang | frozen-kv-mtp 接受 pp_proxy_tensors | [#40355](https://github.com/sgl-project/sglang/pull/40355) | 2026-09-19 |
| Lightning-AI/pytorch-lightning | sampler epoch 在迭代器创建前设置 | [#21960](https://github.com/Lightning-AI/pytorch-lightning/pull/21960) | 2026-09-19 |
| speechbrain/speechbrain | weight_norm parametrizations 静默 deprecation 警告 | [#3087](https://github.com/speechbrain/speechbrain/pull/3087) | 2026-09-19 |
| crewAIInc/crewAI | evaluation 返回 False 替代 True | [#7603](https://github.com/crewAIInc/crewAI/pull/7603) | 2026-09-19 |
| crewAIInc/crewAI | crewai-tools strip UTF-8 BOM | [#7602](https://github.com/crewAIInc/crewAI/pull/7602) | 2026-09-19 |
| MiniMax-AI/MiniMax-M1 | main.py `.to("cuda")` 自动回退 CPU | [#43](https://github.com/MiniMax-AI/MiniMax-M1/pull/43) | 2026-09-20 |
| Vaibhavs10/insanely-fast-whisper | feat: auto-detect Ascend NPU and other non-CUDA accelerat… | [#288](https://github.com/Vaibhavs10/insanely-fast-whisper/pull/288) | 2026-09-21 |
| m-bain/whisperX | feat: auto-detect Ascend NPU and other non-CUDA accelerat… | [#1483](https://github.com/m-bain/whisperX/pull/1483) | 2026-09-21 |
| opendatalab/MinerU | `resolve_batch_output_paths()` 冗余判断 | [#5572](https://github.com/opendatalab/MinerU/pull/5572) | 2026-09-22 |
| chflame163/ComfyUI_LayerStyle | crop mask multiple 设备无关 | [#612](https://github.com/chflame163/ComfyUI_LayerStyle/pull/612) | 2026-09-22 |
| modelscope/DiffSynth-Studio | WanToDance music encoder 设备无关 | [#1708](https://github.com/modelscope/DiffSynth-Studio/pull/1708) | 2026-09-23 |
| fishaudio/fish-speech | extract_vq 用 codec 设备重采样（非硬编码 CUDA） | [#1339](https://github.com/fishaudio/fish-speech/pull/1339) | 2026-09-24 |
| OpenRLHF/OpenRLHF | loss 归一化设备取自 loss mask（非 `torch.cuda`） | [#1365](https://github.com/OpenRLHF/OpenRLHF/pull/1365) | 2026-09-24 |
| jeshraghian/snntorch | fix(loss): apply class weights per sample in the MSE loss… | [#463](https://github.com/jeshraghian/snntorch/pull/463) | 2026-09-25 |
| espnet/espnet | fix(speechlm): make synchronize_batches work on non-CUDA … | [#6808](https://github.com/espnet/espnet/pull/6808) | 2026-09-25 |
| InternLM/xtuner | fix(datasets): build the DP all_reduce tensor on the mesh… | [#2127](https://github.com/InternLM/xtuner/pull/2127) | 2026-09-25 |
| EleutherAI/lm-evaluation-harness | fix(models): point the `hf-audiolm-qwen` lazy mapping at … | [#4244](https://github.com/EleutherAI/lm-evaluation-harness/pull/4244) | 2026-09-26 |
| hpcaitech/ColossalAI | fix: use the accelerator API instead of hard-coded cuda/c… | [#6455](https://github.com/hpcaitech/ColossalAI/pull/6455) | 2026-09-26 |
| espnet/espnet | fix(speechlm): make synchronize_batches() equalize the ba… | [#6813](https://github.com/espnet/espnet/pull/6813) | 2026-09-26 |

## ✅ B 类已合入（37）

| 项目 | 变更 | PR | 合入日期 |
|------|------|----|---------|
| modelscope/FunASR | 去 torchaudio 硬依赖（fbank → kaldi-native-fbank、音频加载 → soundfile、可选导入） | [#3526](https://github.com/modelscope/FunASR/pull/3526) | 2026-08-26 |
| chflame163/ComfyUI_LayerStyle | 设备无关映射（`torch.cuda` → `torch.accelerator`） | [#609](https://github.com/chflame163/ComfyUI_LayerStyle/pull/609) | 2026-09-03 |
| kornia/kornia | RT-DETR device-agnostic map_location | [#4212](https://github.com/kornia/kornia/pull/4212) | 2026-09-05 |
| jeshraghian/snntorch | spikegen.latency 保留输入 dtype | [#445](https://github.com/jeshraghian/snntorch/pull/445) | 2026-09-05 |
| jeshraghian/snntorch | state_quant 保留输入 dtype | [#444](https://github.com/jeshraghian/snntorch/pull/444) | 2026-09-05 |
| fangwei123456/spikingjelly | DSpike surrogate 函数重构兼容（`__init__` 参数顺序错位） | [#748](https://github.com/fangwei123456/spikingjelly/pull/748) | 2026-09-06 |
| kornia/kornia | Z1Projection.unproject 标量 depth 设备/dtype 继承 | [#4340](https://github.com/kornia/kornia/pull/4340) | 2026-09-07 |
| debpalash/VoiceStudio | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1831](https://github.com/debpalash/VoiceStudio/pull/1831) | 2026-09-07 |
| debpalash/VoiceStudio | TTS engine 设备无关（`torch.accelerator` 替代硬编码 CUDA） | [#1830](https://github.com/debpalash/VoiceStudio/pull/1830) | 2026-09-07 |
| jeshraghian/snntorch | `utils.reset(net)` 作用域修复 | [#449](https://github.com/jeshraghian/snntorch/pull/449) | 2026-09-08 |
| OpenADMET/openadmet-models | TabPFN 模型类 accelerator→device 映射修复 | [#601](https://github.com/OpenADMET/openadmet-models/pull/601) | 2026-09-10 |
| vladmandic/sdnext | framepack 用 text_mask.device 替代硬编码 | [#5085](https://github.com/vladmandic/sdnext/pull/5085) | 2026-09-12 |
| kornia/kornia | bbox_to_mask3d 保留输入 dtype | [#4376](https://github.com/kornia/kornia/pull/4376) | 2026-09-13 |
| unslothai/unsloth | sentence_transformer 设备一致性 | [#10843](https://github.com/unslothai/unsloth/pull/10843) | 2026-09-14 |
| unslothai/unsloth | device_type 增加 Ascend NPU 检测 | [#10686](https://github.com/unslothai/unsloth/pull/10686) | 2026-09-14 |
| unslothai/unsloth | chat_templates 移除 CUDA 硬编码设备 | [#10684](https://github.com/unslothai/unsloth/pull/10684) | 2026-09-14 |
| jeshraghian/snntorch | population-code helpers 保留输入 dtype（#428 #429） | [#451](https://github.com/jeshraghian/snntorch/pull/451) | 2026-09-14 |
| kornia/kornia | Boxes 整数坐标按默认 dtype 转浮点 | [#4379](https://github.com/kornia/kornia/pull/4379) | 2026-09-15 |
| hao-ai-lab/FastVideo | AdaLayerNorm autocast 设备无关 | [#1818](https://github.com/hao-ai-lab/FastVideo/pull/1818) | 2026-09-15 |
| chflame163/ComfyUI_LayerStyle | 硬编码 CUDA 节点加 'auto' 设备选项 | [#610](https://github.com/chflame163/ComfyUI_LayerStyle/pull/610) | 2026-09-16 |
| debpalash/VoiceStudio | model_manager 增加 Ascend NPU 支持 | [#2194](https://github.com/debpalash/VoiceStudio/pull/2194) | 2026-09-18 |
| fangwei123456/spikingjelly | `_resolve_device_type` 返回实际 device type | [#755](https://github.com/fangwei123456/spikingjelly/pull/755) | 2026-09-18 |
| jeshraghian/snntorch | fix(export_nir): move tensors to CPU before numpy convers… | [#456](https://github.com/jeshraghian/snntorch/pull/456) | 2026-09-20 |
| kornia/kornia | #4624 | [#4624](https://github.com/kornia/kornia/pull/4624) | 2026-09-20 |
| kornia/kornia | #4371 | [#4371](https://github.com/kornia/kornia/pull/4371) | 2026-09-20 |
| SWivid/F5-TTS | eval faster-whisper 设备无关 | [#1318](https://github.com/SWivid/F5-TTS/pull/1318) | 2026-09-21 |
| kornia/kornia | docs(augmentation): remove incorrect per-channel fill cla… | [#4694](https://github.com/kornia/kornia/pull/4694) | 2026-09-21 |
| vladmandic/sdnext | autoencoder_kl 用 x.device | [#5098](https://github.com/vladmandic/sdnext/pull/5098) | 2026-09-21 |
| modelscope/FunASR | y.device 替代硬编码 .cuda() | [#3710](https://github.com/modelscope/FunASR/pull/3710) | 2026-09-21 |
| unslothai/unsloth | fix(grpo): autocast with DEVICE_TYPE_TORCH instead of a p… | [#11461](https://github.com/unslothai/unsloth/pull/11461) | 2026-09-22 |
| InternLM/lmdeploy | #4986 | [#4986](https://github.com/InternLM/lmdeploy/pull/4986) | 2026-09-22 |
| huggingface/peft | #3734 | [#3734](https://github.com/huggingface/peft/pull/3734) | 2026-09-22 |
| debpalash/VoiceStudio | 设备缓存释放跟随实际加速器 | [#2317](https://github.com/debpalash/VoiceStudio/pull/2317) | 2026-09-24 |
| huggingface/pytorch-image-models | `init_distributed_device_so` 补 `torch.npu.set_device` | [#2801](https://github.com/huggingface/pytorch-image-models/pull/2801) | 2026-09-24 |
| fangwei123456/spikingjelly | fix(neuron): keep GatedLIFNode spike state in the input d… | [#758](https://github.com/fangwei123456/spikingjelly/pull/758) | 2026-09-25 |
| modelscope/ms-swift | Janus 模板 `.cuda()` → `input_ids.device` | [#10230](https://github.com/modelscope/ms-swift/pull/10230) | 2026-09-25 |
| kornia/kornia | fix(geometry): return the exact Euclidean distance instea… | [#4968](https://github.com/kornia/kornia/pull/4968) | 2026-09-26 |

## ❌ B 类关闭未合入（24）

| 项目 | 变更 | PR | 关闭日期 |
|------|------|----|---------|
| vllm-project/vllm-ascend | [BugFix] Fix scheduler dead lock for long requests by add… | [#9543](https://github.com/vllm-project/vllm-ascend/pull/9543) | 2026-05-26 |
| vllm-project/vllm-ascend | [Attention][BugFix] Fix scheduler dead lock for long requ… | [#9549](https://github.com/vllm-project/vllm-ascend/pull/9549) | 2026-05-27 |
| modelscope/FunASR | Make torchaudio import optional in paraformer_v2, fun_asr… | [#3527](https://github.com/modelscope/FunASR/pull/3527) | 2026-08-26 |
| Ascend/pytorch | Register the NPU DTensor RNG tracker and dispatch key | [#165](https://github.com/Ascend/pytorch/pull/165) | 2026-08-29 |
| Stability-AI/stable-audio-tools | Fix apg_project float64 crash on devices without double s… | [#263](https://github.com/Stability-AI/stable-audio-tools/pull/263) | 2026-08-31 |
| DrewThomasson/ebook2audiobook | Fix UnboundLocalError in detect_device by hoisting _norma… | [#2071](https://github.com/DrewThomasson/ebook2audiobook/pull/2071) | 2026-09-07 |
| kornia/kornia | fix(geometry): use math.pi in rad2deg/deg2rad to preserve… | [#4356](https://github.com/kornia/kornia/pull/4356) | 2026-09-08 |
| kornia/kornia | fix(geometry): promote dtype in PinholeCamera.scale_ for … | [#4341](https://github.com/kornia/kornia/pull/4341) | 2026-09-08 |
| ultralytics/ultralytics | fix(results): make cuda() device-agnostic for non-CUDA ac… | [#26202](https://github.com/ultralytics/ultralytics/pull/26202) | 2026-09-17 |
| NousResearch/hermes-agent | fix(model-switch): re-resolve reasoning_config when switc… | [#112924](https://github.com/NousResearch/hermes-agent/pull/112924) | 2026-09-17 |
| open-webui/open-webui | fix(retrieval): use torch.accelerator for ColBERT device … | [#30117](https://github.com/open-webui/open-webui/pull/30117) | 2026-09-18 |
| open-webui/open-webui | fix(retrieval): use torch.accelerator for ColBERT device … | [#30116](https://github.com/open-webui/open-webui/pull/30116) | 2026-09-18 |
| open-webui/open-webui | fix(retrieval): use torch.accelerator for ColBERT device … | [#30114](https://github.com/open-webui/open-webui/pull/30114) | 2026-09-18 |
| crewAIInc/crewAI | fix(llm): register o1/o1-pro/o3 context windows to preven… | [#7604](https://github.com/crewAIInc/crewAI/pull/7604) | 2026-09-19 |
| langchain-ai/langchain | fix(openai): exclude cache-write tokens from service-tier… | [#40692](https://github.com/langchain-ai/langchain/pull/40692) | 2026-09-20 |
| huggingface/accelerate | fix(launch): capture child output in simple_launcher so c… | [#4292](https://github.com/huggingface/accelerate/pull/4292) | 2026-09-21 |
| huggingface/peft | fix: propagate training/eval mode to newly injected adapt… | [#3766](https://github.com/huggingface/peft/pull/3766) | 2026-09-21 |
| huggingface/lerobot | fix(embedder): use device-agnostic default instead of har… | [#4676](https://github.com/huggingface/lerobot/pull/4676) | 2026-09-21 |
| axolotl-ai-cloud/axolotl | fix(kernels): make AMP custom_fwd/bwd device-agnostic | [#3996](https://github.com/axolotl-ai-cloud/axolotl/pull/3996) | 2026-09-22 |
| huggingface/diffusers | minimax 全加速器 autocast | [#14766](https://github.com/huggingface/diffusers/pull/14766) | 2026-09-25 |
| huggingface/diffusers | wan 设备无关默认值 | [#14765](https://github.com/huggingface/diffusers/pull/14765) | 2026-09-25 |
| Lightning-AI/torchmetrics | V-measure 独立聚类返回 0.0 非 1.0 | [#3506](https://github.com/Lightning-AI/torchmetrics/pull/3506) | 2026-09-26 |
| vllm-project/vllm-ascend | [Feature] Enable oproj_tensor_parallel_size for eager mode | [#9737](https://github.com/vllm-project/vllm-ascend/pull/9737) | 2026-09-26 |
| vllm-project/vllm-ascend | add OTP (O-matrix Tensor Parallelism) support for general… | [#9669](https://github.com/vllm-project/vllm-ascend/pull/9669) | 2026-09-26 |

逐条留档见 `EXCLUDED.md` 的「已投 PR 被关闭未合入」段。

## 🔴 需处理（维护者有要求 / 未解决，2026-09-20 核实）

> 以下 PR 有真实维护者 review 或评论需要跟进。⚠️ 状态 2026-09-20 逐一核实：**多数已由晚班 cron 处理到「等维护者 re-review」的正常等待期**，非未处理。真正补做的仅 FunASR #3710 的 try/finally 清理。

| 项目 | PR | 现状（2026-09-20 核实） | 剩余动作 |
|------|----|------|---------|
| [kornia](projects/kornia/) | [#4624](https://github.com/kornia/kornia/pull/4624) | 已补测试 + 修 forward dict 顺序依赖（`c73c2a96`），CI 全绿 | 等 ducha-aiki re-review（晚班跟进） |
| [kornia](projects/kornia/) | [#4371](https://github.com/kornia/kornia/pull/4371) | 已连续回应 10 轮 review（含 float64 dtype 修复，`1ffc2091`） | 等 ducha-aiki re-review（晚班跟进） |
| [docling](projects/docling/) | [#4158](https://github.com/docling-project/docling/pull/4158) | 已按建议改 `.to(self._device, self._model.dtype)`（`0c6fb88`），mergify ready，等 CI+merge | 无（等合并） |
| [lmdeploy](projects/lmdeploy/) | [#4986](https://github.com/InternLM/lmdeploy/pull/4986) | 已修 lazy migration（`887587e`），维护者已认可 | 无 |
| [peft](projects/peft/) | [#3734](https://github.com/huggingface/peft/pull/3734) | 已改用 `infer_device()`（`425afb7`），回应了维护者质疑 | 等 BenjaminBossan re-review（晚班跟进） |
| [PaddleOCR](projects/paddleocr/) | [#18370](https://github.com/PaddlePaddle/PaddleOCR/pull/18370) | CLA 已签（`license/cla: success`），blocked 仅为缺 approve/待合并 | 无（等合并） |

## 🧹 2026-09-27 躺平 / 冲突 / CI 处置（本轮）

> 起因：跟踪的驱动源是 QQ 邮箱通知邮件（**事件驱动**）⇒ 躺平的 PR 不产生邮件、永远看不到。本轮按**时间维度**全量扫 61 个跟踪中 PR（35 个从未有过一条真人评论，7~120 天），处置如下。

| 处置 | PR | 依据（均经 API 回读校验） |
|------|----|------|
| ✅ rebase，冲突已解 | langgenius/dify [#39341](https://github.com/langgenius/dify/pull/39341) | 落后 1828 个提交；冲突仅 `web/global.d.ts`，与 main 新增的 `__marketplaceTracking__` 并存即可 ⇒ `mergeable=true` |
| ✅ rebase + 收窄范围 | ostris/ai-toolkit [#1022](https://github.com/ostris/ai-toolkit/pull/1022) | main 已重构 captioner（`get_caption_for_file` → `_prep_file`/`_caption_item`/`run_caption_loop`），原 librosa 兜底代码已不存在 ⇒ 从 PR 移除，标题/描述同步改为 +21/−3 的 import 守卫 |
| ✅ rebase（落后 2） | Lightning-AI/torchmetrics [#3507](https://github.com/Lightning-AI/torchmetrics/pull/3507) | 干净三方合并；顺带刷新 lit-oss-bot 单测 |
| ✅ 挂 issue 防自动关 | huggingface/diffusers [#14785](https://github.com/huggingface/diffusers/pull/14785) / [#14786](https://github.com/huggingface/diffusers/pull/14786) | repo 的 `pr-link-issue-reminder` 规定：description 无 closing keyword 则提醒后 **10 天自动关闭**（#14765/#14766 即因此被关）。已自建 [#14877](https://github.com/huggingface/diffusers/issues/14877) / [#14878](https://github.com/huggingface/diffusers/issues/14878) 并写入 description |
| ✅ 重跑 CI | m-bain/whisperX [#1469](https://github.com/m-bain/whisperX/pull/1469) | 原 run 被 runner **取消**（test 3.13 起跑 7 秒即中止，其余 3 个 job 同时被取消），非代码失败 ⇒ 推空提交刷新 |
| ⏳ 等维护者加标签 | sgl-project/sglang [#40355](https://github.com/sgl-project/sglang/pull/40355) | `pr-gate` 失败原因就是 `Missing required label 'run-ci'`（仓库规定 fork PR 需维护者加标签）⇒ 已评论请求 |
| ⏸️ 非我方问题 | hao-ai-lab/FastVideo [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) | Mergify 仅在等 `#approved-reviews-by>=1` + `full-suite-passed`（`fastcheck`/`pre-commit` 已绿） |
| ❌ 关闭·僵尸 | vllm-project/vllm-ascend [#9737](https://github.com/vllm-project/vllm-ascend/pull/9737) | 120 天、bot 两次标记冲突、**零人类参与**、落后 2198 个提交 ⇒ 需按当前 OTP 实现重做而非 rebase |
| ❌ 关闭·被取代 | Lightning-AI/torchmetrics [#3506](https://github.com/Lightning-AI/torchmetrics/pull/3506) | 同一 issue #3484 已由上游 #3485 修（master `85f4e168`，09-20 合入，改动与我们逐字相同） |
| 🧹 清理僵尸 job | — | 删除暂停中的 7 点「昇腾PR跟踪检查」、8 点「PyTorch解耦早报」。⚠️ 两者的 **prompt 未成功归档**（备份写入未校验，已确认文件不存在）；其能力仍在：`check_prs.py` 及其状态文件由 21 点 job 继续跑，躺平维度进了 `stale_nudge.py` + 6 点 job 第三步，8 点早报的内容源（mindlog/log）未受影响 |

**机制修正（已落地）**：新增 `scripts/stale_nudge.py`（时间驱动、四桶分类：可温和催办 / 冲突需 rebase / CI 红 / 零真人理会；每 PR 7 天冷却、每轮 ≤3 条、**A 类 pytorch 只报不动**），接入 6 点 job 第三步。
