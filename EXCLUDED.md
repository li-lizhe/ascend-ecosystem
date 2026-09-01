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