# FastVideo — device-type comparison & autocast device-agnostic fixes

**Repo**: [hao-ai-lab/FastVideo](https://github.com/hao-ai-lab/FastVideo) (4.3k★, 93% merge rate, active)
**PR**: [#1817](https://github.com/hao-ai-lab/FastVideo/pull/1817) — fix(metrics): set SceneMetric device_map for any non-CPU device
**PR**: [#1818](https://github.com/hao-ai-lab/FastVideo/pull/1818) — fix(cosmos): make AdaLayerNorm autocast device-agnostic

## 目标 issue

非特定 issue——通过「主动发现 device 假设」扫描 FastVideo 源码发现两处 CUDA 硬编码：

1. `fastvideo/eval/metrics/vbench/scene/metric.py:66` —— `device_map` 仅在
   `self.device.type == "cuda"` 时传入 transformers。
2. `fastvideo/models/dits/cosmos.py:94,134` —— `CosmosAdaLayerNorm`/`CosmosAdaLayerNormZero`
   硬编码 `torch.autocast(device_type="cuda")`。

## 根因

- SceneMetric：非 CUDA 加速器（昇腾 NPU / MPS / XPU / ROCm）上 `device.type == "cuda"`
  恒 False，`device_map` 传 None，Qwen2.5-Omni 模型静默加载到 CPU，metric 在 CPU 上跑。
- Cosmos：`autocast(device_type="cuda")` 只对 CUDA tensor 生效，其他设备上 norm 可能用
  错精度（bf16 而非 fp32），造成精度损失或下游 dtype mismatch。

## 修复

```python
# scene/metric.py
device_map=str(self.device) if self.device.type != "cpu" else None,

# cosmos.py (两处)
with torch.autocast(device_type=hidden_states.device.type, enabled=False):
```

设备无关：`device.type != "cpu"` 对所有加速器都为 True；`autocast(device_type=hidden_states.device.type)`
跟随 tensor 实际设备。两处各改 1-2 行。

## 验证（昇腾 910B2）

- `torch.accelerator.current_accelerator()` → `npu`（torch 2.14.0a0 支持）。
- `torch.device("npu:0").type != "cpu"` → `True`，device_map 会正确传入。
- `torch.autocast(device_type="npu", enabled=False)` 合法且正确为 NPU tensor 关闭 autocast。
- CUDA 行为与原代码一致。

## PR 链接

- https://github.com/hao-ai-lab/FastVideo/pull/1817
- https://github.com/hao-ai-lab/FastVideo/pull/1818
