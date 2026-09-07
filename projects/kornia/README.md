# kornia (kornia/kornia)

Ascend NPU 设备无关适配：三个 device-agnostic 修复，均已在 Ascend 910B 验证。

- 仓库: https://github.com/kornia/kornia (~30700★)
- 活跃度: pushed<1d, 近 30 条 closed merge 率 80% —— 高活跃社区

## PR #4212 — RT-DETR device-agnostic weight loading (已合并)

**状态**: 2026-09-05 已合入

**Fix**: 在 `from_pretrained` 中使用 `torch.accelerator.current_accelerator()` 替代硬编码的 `map_location="cuda"`，让非 CUDA 加速器（NPU/XPU/MPS）也能正确加载权重。

**PR**: https://github.com/kornia/kornia/pull/4212

## PR #4340 — Z1Projection.unproject 标量 depth 的设备/dtype 修复

**问题**: `Z1Projection.unproject` 用 `torch.Tensor([depth])` 创建 CPU float32 张量，不继承 points 的设备（CUDA/NPU/XPU/MPS）和 dtype（float16/bfloat16/float64）
- 在 NPU 上抛出 `Expected all tensors to be on the same device. Expected NPU tensor`
- 在 CPU 上 float16/float64 被静默拓宽到 float32

**修复**: `torch.Tensor([depth])` → `torch.as_tensor([depth], device=points.data.device, dtype=points.data.dtype)`

**验证（Ascend 910B, torch 2.14 + torch_npu）**：旧代码崩溃，新代码通过，CPU float64 回归通过。

**PR**: https://github.com/kornia/kornia/pull/4340 — Fixes #4313
**提交日期**: 2026-09-07（早间新增）

## PR #4341 — PinholeCamera.scale_ 的 int64 height/width dtype 提升

**问题**: `scale_()` 用 `self.height *= scale_factor` 原地写入，把 float 结果写回 int64 存储时报错。

**修复**: `self.height *= scale_factor` → `self.height = self.height * scale_factor`（重新绑定到提升后的 float 张量）

**验证（Ascend 910B, torch 2.14 + torch_npu）**：旧代码崩溃，新代码通过，float32 回归通过。

**PR**: https://github.com/kornia/kornia/pull/4341 — Fixes #4265
**提交日期**: 2026-09-07（早间新增）