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
- **状态**: ⛔ **2026-09-02 未能提交 PR — GitHub PAT (C:\Users\华为\.config\ghtoken) 已失效**（API 恒 401 Bad credentials，与伪造 token 同报错；SSH git push 认证正常）。fork li-lizhe/ComfyUI-KJNodes 无法创建（需 API）。
- **待办**: 恢复 PAT 后 (1) POST /repos/kijai/ComfyUI-KJNodes/forks (2) push 分支 (3) 开 PR body 含 Problem/Root cause/Fix/Verification/Fixes #601 (4) 加入 check_prs.py PRS。
