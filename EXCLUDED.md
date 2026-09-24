# 弃投清单（扫描时跳过——不达标项目）

规则（用户 2026-09-09 重定义）：

1. **提交前筛选（唯一硬门槛）**：最近 14 天是否有人 merge PR —— 有 = 社区正常 review+merge，活项目可投；很久（如 ≥30 天）无任何 merge 的才算僵尸，弃投。**不 care closed 数、不 care merge 率、不以 star 背书**。
2. **提交后持续跟踪**：一旦提交 PR 就持续跟踪到底（直到 merged / closed / 维护者明确拒绝）。
3. **项目排除（动态，check_prs.py 计算）**：7 天内无人真人 review/评论 → `PENDING_7D` 暂停投新 PR，有人响应即恢复；只有 `CLOSED_UNMERGED`（维护者明确不响应）才 `EXCLUDED` 永久不投。**已合入的 repo 永不排除，可继续投**。

本清单列出被「硬门槛」拒绝的僵尸项目，此后扫描跳过。

格式（每行一条）：
- `repo/name — 排除日期 — 原因摘要`

## 已排除（僵尸 / 不达标）

- `Stability-AI/stable-audio-tools — 2026-08-31 — 最近 merge 5-26（90 天无 merge）且 merge 率 47%，PR #263 撤回（踩线不达标）`
- `emelex-ai/BRIDGE — 2026-09-01 — 仅 3 star，不满足影响力门槛（issue #223 device 比较问题本身干净，但项目太小）`
- `fishaudio/fish-speech — 2026-09-01 — 长期无 merge（32k★ 但社区不活跃）`
- `SWivid/F5-TTS — 2026-09-01 — 最近 push 2026-07-23（40 天无 push）`
- `myshell-ai/OpenVoice — 2026-09-01 — 僵尸：最近 push 2025-04-19（500+ 天无 push）`

## 2026-09-03 dtype 金矿线扫描淘汰

- `Kosinkadink/ComfyUI-Advanced-ControlNet — 2026-09-03 — push 36 天前（>30 天门槛），merge 率 93% 但 last merge 36 天`
- `m87-labs/moondream — 2026-09-03 — 僵尸：push 135 天前、merge 率 40%`
- `deepbeepmeep/Wan2GP — 2026-09-03 — merge 率 4/30=13%（9k★ 但大量 close 不合）`
- `ToTheBeginning/PuLID — 2026-09-03 — 僵尸：push 398 天前`
- `1038lab/ComfyUI-JoyCaption — 2026-09-03 — push 252 天前、merge 率 33%`
- `yisol/IDM-VTON — 2026-09-03 — 僵尸：push 544 天前、0 merge`
- `tencent-ailab/IP-Adapter — 2026-09-03 — 僵尸：push 796 天前`
- `nerfstudio-project/nerfstudio — 2026-09-03 — 僵尸：push 400 天前、merge 率 43%，且 #3683 已有竞争 PR #3711`
- `QwenAudio/CosyVoice — 2026-09-03 — push 100 天前、merge 率 27%`
- `kijai/ComfyUI-WanVideoWrapper — 2026-09-03 — push 101 天前`
- `kijai/ComfyUI-SUPIR — 2026-09-03 — push 126 天前、last merge 210 天`
- `Lakonik/ComfyUI-piFlow — 2026-09-03 — merge 率 33%、last merge 104 天、186★`
- `spacepxl/WanTraining — 2026-09-03 — push 418 天前、92★`
- `FlashML-org/FreeToken — 2026-09-03 — merge 率 14/30=47%<50%（踩线不达标）`
- `EnragedAntelope/comfyui-sdnq — 2026-09-03 — push 142 天前、83★`
- `BobJohnson24/ComfyUI-INT8-Fast — 2026-09-03 — push 68 天前、last merge 75 天`
- `yuenhy/stapler — 2026-09-03 — 2★、push 166 天前`
- `krish1925/isotrieve — 2026-09-03 — 5★，影响力不足（维护活跃度本身 PASS）`
- 竞争排除（项目本身活跃，但 issue 已被抢）：`PythonOT/POT #845`（PR #846 已开）、`sbi-dev/sbi #1954`（维护者分配 BHARATH0153，PR #1972）、`verl #7092`（内部认领中）、`fla-org/flash-linear-attention`（NPU 路线由专职团队主导，Ascend PR 均为团队产出）、`ModelTC/LightX2V #1439`（已被我们昨日 PR #1470 覆盖）、`nerfstudio #3683`（PR #3711）

## 已投 PR 被关闭未合入（CLOSED_UNMERGED，原因已核实 2026-09-25）

**B 类 19 个按原因分四类**：
- ① 被上游明确否掉 **3**：accelerate #4292（技术否决，点名软 PR）、ultralytics #26202（设计取向）、peft #3766（未预先认领）
- ② bot/流程秒关 **4**：langchain #40692、open-webui #30114/#30116/#30117
- ③ 自己关·重复撞车 **3**：crewAI #7604、kornia #4356、hermes-agent #112924
- ④ 自己关·并入/被取代/转移/撤回 **9**：axolotl #3996、kornia #4341、FunASR #3527、vllm-ascend #9543/#9549、lerobot #4676、Ascend/pytorch #165、stable-audio-tools #263、ebook2audiobook #2071（维护者自修）
> 真正被社区否决的只有 3 个；撞车/重复占 8 个 → **提交前查重 + 先认领 issue 这条纪律是硬的**。

以下是我们提交的 PR 被上游关闭且未合入（原因各异，留档）：

- `DrewThomasson/ebook2audiobook #2071 — 2026-09-07 关闭 — Fix UnboundLocalError in detect_device（维护者未响应/关闭）｜原因：维护者关：新版本已自行修复（`fixed already on the next version`）`
- `kornia/kornia #4341 — 2026-09-08 关闭 — PinholeCamera dtype 提升（已由 #4371 替代）｜原因：自己关：由 #4371 替代（#4371 已合入）`
- `kornia/kornia #4356 — 2026-09-08 关闭 — rad2deg/deg2rad 用 math.pi｜原因：自己关：#4358 已覆盖同一修复（撞车）`
- `modelscope/FunASR #3527 — 2026-08-26 关闭 — paraformer torchaudio 可选化（与 #3526 冲突，主 PR 已合入）｜原因：自己关：并入 #3526（#3526 已合入）`
- `open-webui/open-webui #30114/#30116/#30117 — 2026-09-18 关闭 — ColBERT torch.accelerator（owui-terminator[bot] 流程秒关：需 target dev 分支 + CLA checkbox + 关联 issue + maintainer 明确邀请 checkbox，自动流水线无法获得维护者邀请，非维护者不采纳）｜原因：`owui-terminator[bot]` 秒关（需 dev 分支+CLA+关联 issue+维护者邀请）`
- `ultralytics/ultralytics #26202 — 2026-09-17 关闭 — results cuda() 设备无关化｜原因：维护者 glenn-jocher **设计否决**：`.cuda()` 命名即目标设备，不做设备无关化`
- `Stability-AI/stable-audio-tools #263 — 2026-08-31 关闭 — apg_project float64 修复（僵尸项目，已排除）｜原因：自己关：内部复核后撤回（僵尸项目）`
- `crewAIInc/crewAI #7604 — 2026-09-19 关闭 — o1/o3 context window 注册（撞车）｜原因：自己关：已被 #7354/#7323/#7411 覆盖（撞车）`
- `vllm-project/vllm-ascend #9543 — 2026-05-26 关闭 — [BugFix] Fix scheduler dead lock for long requests by adding admissio…｜原因：自己关：由 #9549 取代`
- `vllm-project/vllm-ascend #9549 — 2026-05-27 关闭 — [Attention][BugFix] Fix scheduler dead lock for long requests by addi…｜原因：自己关：5 月旧 PR，问题已不再复现（维护者问“这个问题还有吗”后关闭）`
- `Ascend/pytorch #165 — 2026-08-29 关闭 — Register the NPU DTensor RNG tracker and dispatch key｜原因：自己关：正式评审迁至 GitCode MR（GitHub 是镜像）`
- `NousResearch/hermes-agent #112924 — 2026-09-17 关闭 — fix(model-switch): re-resolve reasoning_config when switching models｜原因：自己关：与已合入的 #113117 重复`
- `open-webui/open-webui #30117 — 2026-09-18 关闭 — fix(retrieval): use torch.accelerator for ColBERT device selection｜原因：`owui-terminator[bot]` 秒关（同上）`
- `open-webui/open-webui #30116 — 2026-09-18 关闭 — fix(retrieval): use torch.accelerator for ColBERT device selection｜原因：`owui-terminator[bot]` 秒关（同上，同一改动开 3 个 PR）`
- `langchain-ai/langchain #40692 — 2026-09-20 关闭 — fix(openai): exclude cache-write tokens from service-tier input counts｜原因：`github-actions[bot]` 秒关（无真人 review；缺关联 issue）`
- `huggingface/accelerate #4292 — 2026-09-21 关闭 — fix(launch): capture child output in simple_launcher so callers can i…｜原因：维护者 albertvillanova **技术否决**：未修 #4277 且破坏 `accelerate launch`（静默吞掉子进程输出）`
- `huggingface/peft #3766 — 2026-09-21 关闭 — fix: propagate training/eval mode to newly injected adapter modules｜原因：维护者 BenjaminBossan 关闭：**未预先认领**，issue 提出者自己要做`
- `huggingface/lerobot #4676 — 2026-09-21 关闭 — fix(embedder): use device-agnostic default instead of hardcoded "cuda"｜原因：维护者关：被我们自己的 #4677 取代（#4677 仍 open）`
- `axolotl-ai-cloud/axolotl #3996 — 2026-09-22 关闭 — fix(kernels): make AMP custom_fwd/bwd device-agnostic｜原因：自己关：AMP kernels 改动并入 #3995（#3995 已合入）`
- `pytorch/pytorch #193347 — 2026-08-13 关闭 — [Testcase Refactoring] Add NPU/PrivateUse1 support to common_fsdp.py`