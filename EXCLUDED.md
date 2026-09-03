# 弃投清单（扫描时跳过——不达标项目）

规则（用户 2026-08-31 定）：

1. **提交前筛选（硬门槛）**：repo 30 天内无 push、或近 30 条 closed 合并率 <50%、或近 90 天无 merge 的「僵尸/低响应」项目，一律跳过不投——不为僵尸项目做贡献。
2. **提交后持续跟踪**：一旦提交 PR 就持续跟踪到底（直到 merged / closed / 维护者明确拒绝），不设 7 天排除、不因「N 天无合入」弃投。

本清单列出被「硬门槛」拒绝的项目，此后「每天一 PR」扫描跳过。

格式（每行一条）：
- `repo/name — 排除日期 — 原因摘要`

## 已排除

- `Stability-AI/stable-audio-tools — 2026-08-31 — merge 率 47%<50% 且最近 merge 5-26（90 天无 merge），PR #263 撤回（踩线不达标）`
- `emelex-ai/BRIDGE — 2026-09-01 — 仅 3 star，不满足影响力门槛（issue #223 device 比较问题本身干净，但项目太小）`
- `fishaudio/fish-speech — 2026-09-01 — 近 30 条 closed merge 12/30=40%<50%（32k★ 但 merge 率不达标）`
- `SWivid/F5-TTS — 2026-09-01 — 最近 push 2026-07-23（40 天无 push >30 天门槛）`
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