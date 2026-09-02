# ComfyUI-KJNodes — WanVideoNAG dtype mismatch (issue #601)

- **Repo**: kijai/ComfyUI-KJNodes (3.2k★, 活跃: pushed 2026-08-29, 近30条 closed PR merge 率 53%, 最近 merge 2026-08-10) — 通过硬门槛
- **Issue**: [#601](https://github.com/kijai/ComfyUI-KJNodes/issues/601) "WanVideoNAG - RuntimeError: mat1 and mat2 must have the same dtype"（Half vs BFloat16），0 维护者回复，无 open PR 修复，无人认领
- **根因**: `WanVideoNAG.patch()` 在 patch 时用 `mm.unet_dtype()` 把 conditioning 烘焙成一次性 nag_context；当 diffusion model 实际运行 dtype 与 unet_dtype 不一致（issue 日志: model weight dtype fp16，unet_dtype 默认 bf16）时，`_wan_compute_attention` 里 k/v 与 live query dtype 不匹配，SDPA/matmul 抛错。同类报告: distilled/lightx2v fp16 模型 (issue 评论)。
- **修复**（device 无关，+2 行）: `nodes/model_optimization_nodes.py::_wan_compute_attention` 中 `k = self.norm_k(self.k(context)).to(query.dtype); v = self.v(context).to(query.dtype)`。dtype 一致时为 no-op。
- **昇腾验证**（910B, torch 2.14 + torch_npu, 容器 npu-lizhe）:
  - 复现: bf16 cross_attn 权重 + fp16 query + bf16 nag_context → `RuntimeError: Expected query, key, and value to have the same dtype ... Half and BFloat16`（与 issue 同型）
  - 修复后: 正常前向 (2,128,64) fp16
  - 数值等价: dtype 已匹配路径 allclose=True
- **分支**: 本地 `D:\code\mindlog\xql\ComfyUI-KJNodes` 分支 `fix/wan-nag-dtype-mismatch`（commit aec5dbb）
- **状态**: ✅ 已提交 PR [#749](https://github.com/kijai/ComfyUI-KJNodes/pull/749)（2026-09-02，PAT 恢复后完成 fork + push + 开 PR）
- **tracking**: check_prs.py key `kjnodes-PR`
