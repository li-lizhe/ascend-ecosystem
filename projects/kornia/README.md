# kornia — RT-DETR device-agnostic weight loading

**Repo**: [kornia/kornia](https://github.com/kornia/kornia) (11.3k★, 100% merge rate, active)
**PR**: [#4212](https://github.com/kornia/kornia/pull/4212) — fix(rt_detr): use device-agnostic map_location in from_pretrained

## 目标 issue

非特定 issue——通过「主动发现 device 假设」扫描 `kornia/models/` 发现
`RTDETR.from_pretrained()` 硬编码 `map_location="cuda:0" if torch.cuda.is_available() else "cpu"`。

## 根因

kornia 要求 `torch>=2.5.1`（`torch.accelerator` 必存在），但 `rt_detr/model.py` 的
`from_pretrained` 仍用 CUDA 专属的 `torch.cuda.is_available()` 决定加载目标设备。
在非 CUDA 加速器（昇腾 NPU / 英特尔 XPU / Apple MPS）上要么把权重放到错误设备、
要么退回 CPU，造成多余拷贝或设备不匹配错误。其余 models（base.py/dexined/yunet）
均用 `map_location="cpu"` 或传入 device，唯独 rt_detr 硬编码 cuda。

## 修复

```python
device = str(torch.accelerator.current_accelerator()) if torch.accelerator.is_available() else "cpu"
state_dict = load_state_dict_from_url(URLs[model_name], map_location=device)
```

设备无关：`torch.accelerator.current_accelerator()` 在运行时发现当前加速器，
CUDA→"cuda"、NPU→"npu"、无加速器→"cpu"。改动 6 行。

## 验证（昇腾 910B2）

- 容器 npu-lizhe（torch 2.14.0a0 + torch_npu）：`str(torch.accelerator.current_accelerator())` 返回 `"npu"`
- `torch.load(..., map_location="npu")` 直接把权重加载到 NPU
- CPU 回退路径保持原语义

## 状态

2026-09-04 提交，PR open，待 review。
