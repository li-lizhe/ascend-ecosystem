# GPT-SoVITS — 导出脚本 device 无关加速器检测

**Repo**: [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) (61.5k★, 53% merge rate, pushed 17 天前)
**PR**: [#2837](https://github.com/RVC-Boss/GPT-SoVITS/pull/2837) — fix(export_torch_script_v3v4): device-agnostic accelerator detection

## 目标 issue

项目有 67 个 open 的 NPU/Ascend 相关 issue（用户真实需求强）。通过「主动发现 device 假设」
扫描 `GPT_SoVITS/` 发现 `export_torch_script_v3v4.py` 顶层硬编码
`device = "cuda" if torch.cuda.is_available() else "cpu"`。

## 根因

该脚本把模块级 `device` 变量用于所有张量分配（mel_basis、hann_window、rope、
模型 `.to(device)` 等）。用 CUDA 专属的 `torch.cuda.is_available()` 判定设备，
在非 CUDA 加速器上会把所有张量放到 CPU，静默禁用加速器加速，造成严重卡顿。

## 修复

```python
if hasattr(torch, "accelerator") and torch.accelerator.is_available():
    device = str(torch.accelerator.current_accelerator())
else:
    device = "cuda" if torch.cuda.is_available() else "cpu"
```

用 `hasattr` 守卫保证 PyTorch < 2.5 仍走原 CUDA-or-CPU 回退，向前兼容。改动 9 行。

## 验证（昇腾 910B2）

- 容器 npu-lizhe（torch 2.14.0a0 + torch_npu）：`str(torch.accelerator.current_accelerator())` 返回 `"npu"`
- device="npu" → 张量放 NPU 而非 CPU
- PyTorch < 2.5 回退路径不变

## 状态

2026-09-04 提交，PR open，待 review。
