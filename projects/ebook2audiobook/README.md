# ebook2audiobook

- **上游仓库**: `DrewThomasson/ebook2audiobook`（~20000★，非华为主导，作者 Drew Thomasson）
- **目标 issue**: #2066 `check_device_info() failed during installation: UnboundLocalError`
- **类型**: 设备检测作用域缺陷（纯 Python bug，device 无关）
- **PR**: [#2071](https://github.com/DrewThomasson/ebook2audiobook/pull/2071)（open）
- **分支**: `fix-unboundlocal-normalize-version` @ `d010189`

## 根因

`detect_device()` 里 `_normalize_version()` 被定义在 **ROCm 分支**内：

```python
elif has_rocm() and has_amd_gpu_pci():
    def _normalize_version(v: str) -> tuple:
        ...
```

但 **CUDA 分支**（line 845/887 的 `tag_ver = _normalize_version(ver_str)`）也调用它。
于是任何走 CUDA 路径（CUDA toolkit + NVIDIA GPU / WSL2）却非 ROCm 的机器，函数从未被绑定，
`check_device_info()` 在安装时抛 `UnboundLocalError`。用户在 aarch64 Linux（无独显路径）踩中，
这正是昇腾 aarch64 场景同源。

## 修复

把唯一一份定义提升到 `detect_device()` 函数体顶层，与其它 helper 闭包
（`lib_version_parse` / `version_classify` 等）并列，使所有设备分支可见。
纯作用域修复，无行为变化。diff **+10/−10（20 行）**。

## 验证

- `python -m py_compile lib/classes/device_installer.py` 通过。
- 非 ROCm 机器端到端跑 `detect_device()`：返回 `('xpu','xpu',...)` 不崩（Intel oneAPI/XPU 路径）。
- AST 校验：`_normalize_version` 现在是 `detect_device` 函数体顶层定义，不再嵌套于任何 if/elif。

> 说明：昇腾 NPU 无 NVIDIA，不触发 CUDA 分支，此 bug 无法在 910B 上复现；
> 但修复是确定性作用域提升（AST 已证明），且与本机端到端 + 语法三重验证闭环。