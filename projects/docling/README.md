# Docling · dtype mismatch 修复

[docling-project/docling](https://github.com/docling-project/docling)（65.9k★）文档解析引擎，HF transformers 图片分类/目标检测推理引擎在非默认 `torch_dtype`（bfloat16 等）下输入 dtype 未对齐导致 matmul 崩溃。

## 问题

配置 `picture_engine_options.torch_dtype = "bfloat16"` 后，模型权重按 bf16 加载（`from_pretrained(dtype=bf16)`），但 HF 预处理器仍输出 float32 输入 → `predict_batch()` 仅 `.to(self._device)` 未转 dtype → 推理崩溃：

```
RuntimeError: mat1 and mat2 must have the same dtype, but got Float and BFloat16
```

关联上游 issue：[#3110](https://github.com/docling-project/docling/issues/3110)

## 根因

`image_classification/transformers_engine.py` 与 `object_detection/transformers_engine.py` 的 `predict_batch()` 中，预处理张量只移到设备、未对齐模型权重 dtype。

## 修复

在 `.to(self._device)` 后，将浮点输入张量 cast 到 `self._model.dtype`；整数张量（如 `pixel_mask`）保持不变（不参与 matmul）。两个引擎同模式一并修复。device-agnostic（用 `self._model.dtype`，无任何 `if cuda/npu` 分支）。

## 验证

- 昇腾 910B（torch 2.14.0a0 + CANN）实测：修复前 float32 × bf16 权重被 NPU auto-promote（无报错但有性能/内存浪费）；修复后 pixel_values 正确 cast 为 bf16 与权重匹配，matmul 成功，`pixel_mask`（int64）保持原样。
- 逻辑自洽：`torch.is_floating_point` 过滤确保只转浮点张量。

## 上游 PR

- **PR #4158**：fix: align transformer engine input dtype with model weights (fixes #3110)
  https://github.com/docling-project/docling/pull/4158

### 2026-09-04 晚间 — DCO 修复

DCO 检查失败（commit 缺少 Signed-off-by）。已添加 remediation commit（`DCO Remediation Commit for li-lizhe <147392333@qq.com>`），DCO 检查已通过（success）。所有 4 项 CI 检查（Mergify、lint-and-type、dco_advisor、DCO）均通过，PR ready to merge。
