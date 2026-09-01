# LightX2V — PR #1470

- Repo: `ModelTC/LightX2V`（清华 ModelTC，非华为）
- Star: ~2.8k ｜ 近 30 closed merge 率 29/30 = 97% ｜ 2026-09-01 当天活跃 push
- Issue: #1439 "Qwen-Image-Edit-2509 Scaled FP8 inference fails with BF16/FP8 dtype mismatch on RTX A6000"
- PR: https://github.com/ModelTC/LightX2V/pull/1470
- head: `li-lizhe:fix-pre-weights-dit-quant-scheme`

## 类型
FP8 预量化 checkpoint 下 dtype mismatch（device-agnostic scheme 分发不一致）—— 与 musubi-tuner #1076 同款「量化权重路径 dtype 未对齐」class。

## 根因
`ZImagePreWeights`（pre_weights.py）把 img_in / txt_in / timestep embedder 硬编码为
`MM_WEIGHT_REGISTER["Default"]`，而 `ZImagePostWeights` 与 `ZImageTransformerWeights`
均跟随 `config["dit_quant_scheme"]`。跑预量化 fp8 checkpoint（e.g.
qwen_image_edit_2509_fp8_e4m3fn_scaled）时，all_x_embedder 以 float8_e4m3fn 加载，
却走 Default 的 `torch.addmm` → bf16 激活 × fp8 权重 → dtype mismatch。

## 修复
pre_weights.py 加 `self.mm_type = config.get("dit_quant_scheme", "Default")`，
4 个 mm 层（img_in / txt_in / time_text_embed_linear_1 / linear_2）改注册
`MM_WEIGHT_REGISTER[self.mm_type]`，与 post/transformer 对齐。+5 / -4 行。

## 验证
- `py_compile` 通过。
- AST 断言：4 个 mm 层均 follow `self.mm_type`，与 `ZImagePostWeights` 行为一致。
- 昇腾/report 环境（无 CUDA fp8 kernel）无法端到端复现 —— fp8-sgl 的 apply 依赖
  CUDA `torch.ops._C.cutlass_scaled_mm`（SM89+）。此为 scheme 分发一致性修复，
  昇腾 NPU 跑 fp8 scaled 推理同样会先踩这个 Default-addmm dtype mismatch。