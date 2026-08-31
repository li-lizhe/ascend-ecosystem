# stable-audio-tools

## PR #263 — apg_project float64 崩溃 + Gradio 切片 TypeError（Fixes #261）

- **项目**：Stability-AI/stable-audio-tools（3851★，2026-05 起低频但近期有维护 push，8-21 有 push）
- **Issue**：[#261](https://github.com/Stability-AI/stable-audio-tools/issues/261) — run_gradio.py 在 MPS 上首次生成就崩（float64 无支持），另含设备无关的 float 切片 TypeError
- **根因**：
  1. `apg_project()` 无条件 `.double()`，MPS 无 float64 → TypeError（默认 `apg_scale=1.0` 必触发）
  2. `seconds_total` 从 Gradio Slider 来是 Python float，`audio[:,:,:seconds_total*sample_rate]` 切片必须 int → 任何设备都崩
- **修复**（8 insertions / 3 deletions，2 文件）：
  1. `precise_dtype = torch.float32 if v0.device.type == "mps" else torch.float64`，投影中间精度按设备支持选择，CUDA/CPU 行为不变，输出仍 cast 回原 dtype
  2. 切片加 `int()` 截断
- **验证**（昇腾 910B / 容器 npu-lizhe / torch 2.14.0a0 + torch_npu，aarch64）：
  - 新旧 `apg_project` 输出 CPU/NPU 均 **bit-identical**（max|Δ|=0），带/不带 padding_mask 均一致
  - 正交性不变式 `<o, v1> ≈ 0` 成立（NPU 上 1.3e-06）
  - 旧行为 float 切片确实抛 TypeError/IndexError；`int()` 后 shape 正确 `(1,2,128000)`
- **PR**：https://github.com/Stability-AI/stable-audio-tools/pull/263 — head `li-lizhe:fix-apg-float64-slice`，Fixes #261
- 本地仓库：`D:\code\mindlog\xql\sat-fix`（分支 fix-apg-float64-slice），验证脚本 `verify_apg.py`
- 提交日期：2026-08-31
