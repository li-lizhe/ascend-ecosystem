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

**Review 反馈处理**（ducha-aiki, 2026-09-07）：已按 review 完成 P1 回归测试（`test_unproject_scalar_depth`）、P1 CHANGELOG 条目、P2 docstring 更新，PR body 措辞已修正，push 到分支并回复（32401b26）。

## PR #4341 — PinholeCamera.scale_ 的 int64 height/width dtype 提升（已关闭，功能迁移至 #4371）

**问题**: `scale_()` 用 `self.height *= scale_factor` 原地写入，把 float 结果写回 int64 存储时报错。

**修复**: `self.height *= scale_factor` → `self.height = self.height * scale_factor`（重新绑定到提升后的 float 张量）

**验证（Ascend 910B, torch 2.14 + torch_npu）**：旧代码崩溃，新代码通过，float32 回归通过。

**PR**: https://github.com/kornia/kornia/pull/4341 — Fixes #4265
**提交日期**: 2026-09-07（早间新增）
**关闭原因**: 2026-09-08 主动关闭，功能迁移至 PR #4371（review 要求改方案，原地 `*=` 改为 `self.height = self.height * scale_factor` 重绑定）

**Review 反馈处理**（ducha-aiki, 2026-09-07）：已按 review 完成 P1 回归测试（`test_scale_inplace_int64_size`）、P1 CHANGELOG 条目（标注 height/width 重绑定的副作用）、P1 PR body 副作用说明（#4264 保持 open）、P2 docstring 更新，push 到分支并回复（5f1a61c6）。PR 叠在 #4340 之上，待 #4340 合入后 rebase。

## PR #4356 — rad2deg/deg2rad 用 math.pi 保留全精度（已关闭）

### 目标 issue
- [#3937](https://github.com/kornia/kornia/issues/3937) — 整数输入时 `pi` 被截断为 3（结果偏 5%）；float64 输入丢 ~7 位有效数字

### 根因
`rad2deg/deg2rad` 用 `pi.to(device).type(tensor.dtype)` 将 float32 常数强转成输入 dtype：整数输入 → `pi=3`；float64 → 从已截断的 float32 再升精度，丢失的信息无法恢复。

### 修复
改用 `math.pi`（Python double，全精度），删除 `pi.to(device).type(dtype)` 强转。仅 `kornia/geometry/conversions.py` 改 3+/2-（新增 `import math`）。

### 昇腾验证（Ascend NPU）
- `rad2deg(torch.tensor([1,2,3]))` → `[57.2958, 114.5916, 171.8873]`（修复前为 `[60,120,180]`）
- `rad2deg(torch.tensor(math.pi, dtype=torch.float64))` → `180.0`（<1e-10 误差）
- 结果与 NumPy `np.degrees` 一致；设备位置保持

### PR
- PR #4356 Fix `rad2deg`/`deg2rad` to use `math.pi` for full precision — https://github.com/kornia/kornia/pull/4356（Fixes #3937）
- **提交日期**: 2026-09-08（早间新增收尾）

## PR #4376 — bbox_to_mask3d 保留输入 dtype（open，等待 review）

### 目标 issue
- [#4250](https://github.com/kornia/kornia/issues/4250) — `bbox_to_mask3d` 无条件返回 float32，不保留输入 dtype（`bbox_to_mask`/`Boxes3D.to_mask` 都保留）

### 根因
`bbox_to_mask3d` 用 `return m.float()` 硬编码 float32 输出；2D 版本 `bbox_to_mask` 用 `mask.to(boxes.dtype)` 正确保留输入 dtype。

### 修复
`return m.float()` → `return m.to(boxes.dtype)`。仅改 1 行 + docstring（去 4250 wart 引用）+ 测试改名断言新行为。

### 昇腾验证（Ascend NPU, torch 2.14 + torch_npu）
- float32→float32, float16→float16, int64→int64, float64→float32（NPU 不支持 double 自动钳制，与 `bbox_to_mask` 同约束）
- mask 数值不变（unit cube: interior 全1、z=0 全0、sum=8）

### PR
- PR #4376 fix(geometry): make `bbox_to_mask3d` preserve the input dtype — https://github.com/kornia/kornia/pull/4376（Fixes #4250）
- **提交日期**: 2026-09-09（早间新增）

## PR #4379 — Boxes/Boxes3D 整数坐标按默认 dtype 转浮点（而非硬编码 float32）

### 目标 issue
- [#4012](https://github.com/kornia/kornia/issues/4012) — `Boxes(...)` 默认拒绝整数坐标，而 `from_tensor` 静默 `float()` 转 float32，无视 `torch.get_default_dtype()`，两种 dtype 策略不一致。

### 根因
5 处 `.float()` 硬编码把整数输入强转 float32，忽略用户配置的默认浮点 dtype（`torch.get_default_dtype()`）。

### 修复
5 处 `.float()` → `.to(torch.get_default_dtype())`，让整数→浮点转换尊重默认 dtype：
- `_transform_boxes`（boxes.py:62）
- `_boxes_to_quadrilaterals`（boxes.py:114）
- `Boxes.__init__`（boxes.py:293）
- `Boxes3D.__init__`（boxes.py:1211）
- `_boxes_to_hexahedrons`（boxes.py:1317）

### 验证
- `py_compile` 通过。
- 默认 dtype float32 下行为不变（转 float32）；`torch.set_default_dtype(torch.float64)` 下整数输入转 float64。

### PR
- PR #4379 fix: cast integer boxes to default dtype instead of hardcoded float32 — https://github.com/kornia/kornia/pull/4379（Fixes #4012）
- **提交日期**: 2026-09-09（手工新增）