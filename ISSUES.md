# ISSUES.md — 我方提的 open issue（邮件哨兵识别用，由 `issues_build.py` 全量重建）

维护者可直接在这些 issue 下回复（不走 PR review）。本文件登记后，
`pr_mail_scan.py` 才会把这类通知当事件报出，而不是静默丢弃。

## 跟踪中

| 仓库 | 标题 | 链接 | 建 | 更新 | 评论 | 标签 |
|---|---|---|---|---|---|---|
| EleutherAI/lm-evaluation-harness | hf-audiolm-qwen: `generate_until` hardcodes `.to("cuda")` an | [#4256](https://github.com/EleutherAI/lm-evaluation-harness/issues/4256) | 2026-09-27 | 2026-09-27 | 0 | - |
| EleutherAI/lm-evaluation-harness | `hf-audiolm-qwen` is unusable: MODEL_MAPPING points at a cla | [#4243](https://github.com/EleutherAI/lm-evaluation-harness/issues/4243) | 2026-09-26 | 2026-09-26 | 0 | - |
| InternLM/xtuner | [NPU] reduce_sum_across_dp_group builds the all_reduce tenso | [#2126](https://github.com/InternLM/xtuner/issues/2126) | 2026-09-25 | 2026-09-25 | 0 | - |
| MiniMax-AI/MiniMax-M1 | main.py hard-codes CUDA and crashes on CPU/Ascend/NPU machin | [#44](https://github.com/MiniMax-AI/MiniMax-M1/issues/44) | 2026-09-20 | 2026-09-20 | 0 | - |
| NVlabs/Sana | LongSana hardcodes CUDA/NCCL for distributed init and FSDP d | [#513](https://github.com/NVlabs/Sana/issues/513) | 2026-09-28 | 2026-10-17 | 1 | - |
| Vaibhavs10/insanely-fast-whisper | CLI hard-codes CUDA when --device-id is an integer, breaking | [#287](https://github.com/Vaibhavs10/insanely-fast-whisper/issues/287) | 2026-09-21 | 2026-09-21 | 0 | - |
| Wan-Video/Wan2.2 | `import wan` fails on non-CUDA builds: torch.cuda.current_de | [#397](https://github.com/Wan-Video/Wan2.2/issues/397) | 2026-09-28 | 2026-09-28 | 0 | - |
| X-GenGroup/Flow-Factory | [Bug] accelerator RNG state leaks out of seeded blocks on no | [#243](https://github.com/X-GenGroup/Flow-Factory/issues/243) | 2026-10-13 | 2026-10-13 | 0 | - |
| areal-project/AReaL | [BUG] Megatron weight-residency calls torch.cuda.* directly, | [#1786](https://github.com/areal-project/AReaL/issues/1786) | 2026-10-14 | 2026-10-14 | 0 | - |
| hao-ai-lab/FastVideo | [Bug] SP communication warmup hardcodes device="cuda", break | [#1987](https://github.com/hao-ai-lab/FastVideo/issues/1987) | 2026-10-19 | 2026-10-19 | 0 | installation, platform, scope: inference, scope: attention, scope: distributed |
| hpcaitech/ColossalAI | fx tracer / rope init hard-code the device, so NPU runs fall | [#6454](https://github.com/hpcaitech/ColossalAI/issues/6454) | 2026-09-26 | 2026-09-26 | 0 | - |
| huggingface/diffusers | WanAnimatePipeline.get_i2v_mask() defaults device to "cuda", | [#14881](https://github.com/huggingface/diffusers/issues/14881) | 2026-09-27 | 2026-09-27 | 0 | - |
| huggingface/diffusers | `Pipeline.to()` offload guards only cover `cuda`/`xpu`: Asce | [#14878](https://github.com/huggingface/diffusers/issues/14878) | 2026-09-26 | 2026-09-26 | 0 | - |
| huggingface/diffusers | `apply_group_offloading(use_stream=True)` raises on Ascend N | [#14877](https://github.com/huggingface/diffusers/issues/14877) | 2026-09-26 | 2026-09-26 | 0 | - |
| langgenius/dify | Monaco Editor Web Worker always fails with 404 due to missin | [#39340](https://github.com/langgenius/dify/issues/39340) | 2026-07-21 | 2026-07-21 | 1 | - |
| li-lizhe/doc | log | [#1](https://github.com/li-lizhe/doc/issues/1) | 2021-05-31 | 2021-05-31 | 2 | - |
| m-bain/whisperX | CLI and API silently fall back to CPU on Ascend NPU because  | [#1482](https://github.com/m-bain/whisperX/issues/1482) | 2026-09-21 | 2026-10-21 | 1 | - |
| modelscope/FunASR | [dist] XPU distributed backend selection (XCCL / oneCCL) is  | [#3777](https://github.com/modelscope/FunASR/issues/3777) | 2026-10-17 | 2026-10-17 | 1 | - |
| modelscope/modelscope | [Bug] torch_utils distributed helpers hard-code CUDA: init_d | [#1824](https://github.com/modelscope/modelscope/issues/1824) | 2026-10-18 | 2026-10-18 | 1 | - |
| pyannote/pyannote-audio | get_devices() and `--device auto` silently fall back to CPU  | [#2082](https://github.com/pyannote/pyannote-audio/issues/2082) | 2026-10-19 | 2026-10-19 | 1 | - |
| pytorch/pytorch | [Feature Request] Make the fake process group and the LocalT | [#199239](https://github.com/pytorch/pytorch/issues/199239) | 2026-10-01 | 2026-10-01 | 0 | oncall: distributed, triaged, bot-triaged, oncall: distributed infra |
| roboflow/inference | DEVICE autodetect is CUDA-only: models load on CPU on non-CU | [#3233](https://github.com/roboflow/inference/issues/3233) | 2026-10-21 | 2026-10-21 | 0 | - |
| triton-lang/triton-ascend | 【硬件解耦任务】[Bug]: 静态 r-numel 被特化为 ASTSource 编译期常量时，fused softma | [#2531](https://github.com/triton-lang/triton-ascend/issues/2531) | 2026-10-13 | 2026-10-19 | 3 | wait-feedback, autotune, compiler, python, ascend-backend, kernels |
| triton-lang/triton-ascend | 【硬件解耦任务】[Bug]: 归约轴被 split（`R0_BLOCK < rnumel`）时 index 归约丢 ch | [#2530](https://github.com/triton-lang/triton-ascend/issues/2530) | 2026-10-13 | 2026-10-21 | 11 | triaged, compiler, python, ascend-backend, kernels, scripts |
| unslothai/unsloth | RFC: Ascend NPU (昇腾) backend support for unsloth | [#10772](https://github.com/unslothai/unsloth/issues/10772) | 2026-09-11 | 2026-09-11 | 0 | - |
| verl-project/verl-omni | [reward] whisper_cer scorer cannot run on non-CUDA accelerat | [#768](https://github.com/verl-project/verl-omni/issues/768) | 2026-10-16 | 2026-10-16 | 0 | - |

共 26 个 open issue。
