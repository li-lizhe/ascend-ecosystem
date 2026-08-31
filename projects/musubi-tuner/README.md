# musubi-tuner

## PR #1079 — fp8_scaled 非 scaled_mm 路径 dtype mismatch（Fixes #1076）

- **项目**：kohya-ss/musubi-tuner（2005★，非华为，维护者活跃，近 30 条 closed merge 19/20=95%）
- **Issue**：[#1076](https://github.com/kohya-ss/musubi-tuner/issues/1076) — 图像生成 `--fp8_scaled` 在非 `_scaled_mm` 路径崩溃（ROCm 必走此路径）
- **根因**：`fp8_linear_forward_patch` 反量化分支用 `scale_weight.dtype`（fp32）推出 `dequantized_weight`，但 activation 是 bf16/fp16，`F.linear` 报 dtype mismatch。`_scaled_mm` 分支显式传 `out_dtype` 故不受影响。
- **修复**（1 行）：反量化后 `dequantized_weight = dequantized_weight.to(x.dtype)`，对齐 activation dtype
- **验证**（昇腾 910B / 容器 npu-lizhe / torch 2.14.0a0 + torch_npu，aarch64，非 `_scaled_mm` 后端）：
  - 修复前：`F.linear(bf16_x, fp32_w)` 抛 `expected m1 and m2 to have the same dtype`（无 bias）/ `self and mat2 ...`（有 bias）
  - 修复后：输出 `(3,64)` bf16，且 cast 结果与直接用原 bf16 权重计算逐 bit 一致（max|Δ|=0.0）
- **PR**：https://github.com/kohya-ss/musubi-tuner/pull/1079 — head `li-lizhe:fix-fp8-scaled-dtype-mismatch`，Fixes #1076
- 本地仓库：`D:\code\mindlog\xql\musubi-tuner`（分支 fix-fp8-scaled-dtype-mismatch）
- 提交日期：2026-08-31（重新执行筛选后的达标目标）