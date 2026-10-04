# aigc-apps/VideoX-Fun — Z-Image ComfyUI 加载器不认 `model.diffusion_model.` 前缀

- **PR**: https://github.com/aigc-apps/VideoX-Fun/pull/522 (open, 1 file, +6/−0, 1 commit)
- **Issue**: https://github.com/aigc-apps/VideoX-Fun/issues/503
- **Round**: 2026-10-04 晚 21 点探新流水线（178 仓池 · T1）
- **验证等级**: 🟡（本机无 ComfyUI/torch 环境；把仓库原文 `convert_state_dict` + 闸门逐字提取后执行，只 stub 了 tensor 对象）

## 问题

`comfyui/z_image/nodes.py` 里 `LoadZImageTransformerModel.loadmodel` 用裸键判断要不要做
ComfyUI→diffusers 键名转换：

```python
if "x_embedder.weight" in transformer_state_dict.keys():
    transformer_state_dict = convert_state_dict(transformer_state_dict)
```

而 `convert_state_dict` 内部也全部按裸键匹配（`x_embedder.`/`final_layer.`/`.attention.` 等）。
ComfyUI 原生 `diffusion_models/*.safetensors`（例如 CivitAI 的 Z-Image 微调
`cyberrealisticZImage_v70_bf16.safetensors`）把每个 tensor 都存在 **`model.diffusion_model.` 前缀**下，
于是闸门永远不触发、前缀原样留下，严格的 `load_state_dict` 直接报错：

```
RuntimeError: Error(s) in loading state_dict for ZImageTransformer2DModel:
  Missing key(s): x_pad_token, all_x_embedder.2-1.weight, all_final_layer.2-1.weight, ...
  Unexpected key(s): model.diffusion_model.cap_pad_token, model.diffusion_model.x_embedder.weight, ...
```

## 修法

在读取 checkpoint 之后、闸门之前：若**所有**键都带 `model.diffusion_model.` 前缀则统一剥掉，
其余逻辑与转换代码完全不动（裸键 checkpoint 不受影响）。

## 验证（🟡）

把仓库里的 `convert_state_dict` 函数体与闸门语句**逐字提取**执行（不重抄），
喂合成的 ComfyUI 格式 checkpoint；只有 tensor 对象被 stub（只用到 `.chunk(3)`），
键名改写走的是真实代码：

| checkpoint 键风格 | 闸门触发 | 处理后键数 | `load_state_dict(strict=True)` |
| --- | --- | --- | --- |
| 裸键（原本就能用） | 是 | 13 | OK |
| `model.diffusion_model.` 前缀，**修复前** | 否 | 9，前缀保留 | **RuntimeError**：缺 `all_x_embedder.2-1.*` / `all_final_layer.2-1.*`，多 `model.diffusion_model.*` |
| `model.diffusion_model.` 前缀，**修复后** | 是 | 13 | OK，与裸键用例键集完全一致 |

**未测**：真实 ComfyUI 模型加载 / 出图（本机无 ComfyUI 环境）。改动只影响加载器走哪个分支。

## 证据文件

- `verify_z_image_prefix.py` — 复现脚本（从 nodes.py 提取原文逻辑）
- `verification-z-image-prefix.txt` — 原始输出
