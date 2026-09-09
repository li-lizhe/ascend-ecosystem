# openadmet-models (OpenADMET/openadmet-models)

Ascend NPU 设备无关适配：accelerator→device 映射修复，使非 CUDA 加速器（NPU/XPU/MPS）能在 TabPFN 模型上正常使用。

- 仓库: https://github.com/OpenADMET/openadmet-models (~60★)
- 活跃度: pushed<1d, 最近 merge 2026-09-08 —— 活跃

## PR #601 — TabPFN 模型类的 accelerator→device 映射修复

### 目标 issue
- [#589](https://github.com/OpenADMET/openadmet-models/issues/589) — 公开 model API 用 `accelerator`（`"cpu"`/`"gpu"`/`"auto"`），底层框架期望 `device`（`"cuda"`/`"mps"`/`"xla"`），映射不一致。已被 TabICL/ChemProp 修复，tabpfn.py 未处理。

### 根因
`tabpfn.py` 两个模型类用 `accelerator = self.accelerator if self.accelerator != "gpu" else "cuda"` 简单替代，`"auto"` 被直接传成 `device="auto"` 给 TabPFN 估算器——且两类的 `accelerator` `Literal` 类型不一致（`Literal["cpu","gpu","auto"]` vs `Literal["cpu","cuda","auto"]`）。

### 修复
- 新增 `_resolve_device()` 函数，与已合入的 `tabicl.py` 模式一致：`gpu→cuda`、`tpu→xla` 别名映射，`"auto"` 原样通过（TabPFN 原生支持 `device="auto"`，`DevicesSpecification` 类型）。
- 两类 `accelerator` 字段从不相容的 `Literal` 统一拓宽为 `str`，让 `"mps"`、`"cuda:0"` 等可达。
- 新增 `field_validator`，用 `torch.device()` 热切校验解析后的值。
- 两处 `build()` 方法改用 `_resolve_device()`。

### 验证
- `py_compile` 通过。
- 验证器热切拒绝未知 accelerator；`"auto"`/`"gpu"`/`"cuda"`/`"mps"` 均正确解析。

### PR
- PR #601 fix: resolve accelerator to device in TabPFN model classes — https://github.com/OpenADMET/openadmet-models/pull/601（Fixes #589）
- **提交日期**: 2026-09-09（手工新增）