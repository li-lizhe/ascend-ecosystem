# snntorch (jeshraghian/snntorch)

★2040 SNN (Spiking Neural Network) 训练框架。硬门槛 2026-09-03 全 PASS：push 3 天内、近 30 条 closed PR merge 率 22/30=73%、最近 merge 3 天前（PR #432 dtype 系列刚合入）。

## 2026-09-03 — dtype 保持系列（PR #444 / #445）

### 目标 issue
- #439 `state_quant` returns float32 for float64 inputs（0 评论，未认领，作者 GraceDyer 老账号非马甲）
- #440 `spikegen.latency` returns float32 for float64 inputs（0 评论，未认领，同作者，描述专业带最小复现）

背景：维护者正系统性收 dtype 保持系列（PR #432 已 merged、#434 open），此二 issue 是同族未认领项，正合时宜。

### 根因
- **#439** `snntorch/functional/quant.py`：量化电平 `torch.linspace/torch.tensor` 默认 float32，`StateQuant.forward` 只做 `levels.to(device)` 不转 dtype，输出 `levels[idx_match]` 继承 float32。
- **#440** `snntorch/spikegen.py`：模块级 `dtype = torch.float` 硬编码 + `latency_interpolate` 里 `torch.round(x).float()` 显式下转，三处硬编码 float32。

### 修复（设备无关、dtype 无关）
- #439：`levels = levels.to(device=device, dtype=input_.dtype)`（1 行）+ 回归测试。
- #440：`torch.zeros(..., dtype=data.dtype)`；`.float()` → `.to(spike_time.dtype)`；`torch.ones(..., dtype=spike_time.dtype)`。模块级 `dtype` 常量保留给 `to_one_hot` 等整型路径，改动严格限定 latency 路径。

### 昇腾验证（177 / npu-lizhe 容器，torch 2.14.0a0 + torch_npu 910B）
- latency 4 条路径（default/normalize/linear+normalize/interpolate+normalize）× {cpu, npu} × {f32, f64} dtype 全保持；bf16 在 NPU 上也正确保持。
- state_quant 3 种模式 × {cpu, npu} × {f32, f64} 全过（NPU f32）。
- 数值等价：f64 与 f32 输出逐元素一致；STE 梯度 float64 正常回流。
- e2e：latency 编码 → Linear → Leaky 神经元在 npu:0 上 dtype/设备正确。
- 已知限制（非本次引入）：NPU 上 float64 `aclnnMinDim` 报 DT_DOUBLE 不支持（torch_npu 算子覆盖限制），修复前后行为一致（pre-fix 复现确认）。

### PR
- PR #444 Fix state_quant to preserve the input tensor's dtype — https://github.com/jeshraghian/snntorch/pull/444（Fixes #439）
- PR #445 Fix spikegen.latency to preserve the input tensor's dtype — https://github.com/jeshraghian/snntorch/pull/445（Fixes #440）

分支：li-lizhe/snntorch `fix/state-quant-dtype` / `fix/latency-dtype`（基于 master 83e1d15）。

### 备注
两 issue 同族但代码路径独立（quant.py vs spikegen.py），按 skill「小量多次分批提交」原则拆成两个 PR。

### 2026-09-04 晚间 — CI 修复

维护者 @ixfd64 指出 #444 的 CI 测试失败。根因：PR #444 和 #445 共享了相同的测试文件 `test_quant_dtype.py`，该文件同时测试了 `latency` 和 `state_quant`。PR #444（只修 state_quant）包含了 latency 测试但无 latency 修复 → latency 测试失败。

**修复**：从 #444 的测试文件中移除 `test_latency_preserves_dtype`（该测试正确属于 #445）。已 push 修复并回复维护者。

## 2026-09-08 — PR #449 `reset(net)` 作用域修复

### 目标 issue
- [#438](https://github.com/jeshraghian/snntorch/issues/438) — `utils.reset(net_a)` 会顺带清零另一个独立网络 `net_b` 的隐藏状态

### 根因
`reset()` → `_layer_check()` → `_layer_reset()` 调用类级 `cls.reset_hidden()`（@classmethod），它遍历 `cls.instances`——**该类的全部实例注册表**，而非 `net` 内所属模块

### 修复
保留全局 flags 与 `_layer_check()`（供 `backprop.py` 读取），把类级 `_layer_reset()` 替换为直接遍历 `net.modules()` 调用实例级 `reset_mem()`，将 reset 限定在传入网络内。仅 `snntorch/utils.py` 改 18+/4-。

### 昇腾验证（177 / npu-lizhe 容器，torch 2.14.0a0 + torch_npu 910B）
- 修复前：`reset(net_a)` 后 `net_b` mem 也被清零（BUG CONFIRMED）
- 修复后：`net_a` 清零、`net_b` 保持原值（PASS）
- 回归：3 步独立 forward/backward/step/reset 循环正常，无 NaN

### PR
- PR #449 Fix `utils.reset(net)` to scope reset to the given network — https://github.com/jeshraghian/snntorch/pull/449（Fixes #438）

## 2026-09-10 — PR #451 population-code dtype 保持

### 目标 issue
- #428 `ce_rate_loss` / `ce_count_loss` 在 population_code=True 时，float64 输入/权重报 `RuntimeError: expected scalar type Float but found Double`
- #429 `accuracy_rate` 在 population_code=True 时，float64 相近分数精度丢失、报错类别

### 根因
- `loss.py` 模块级 `dtype = torch.float` 硬编码 float32
- `loss.py` / `acc.py` 的 `_population_code` 用 `torch.zeros(...)` 默认 float32 建累积张量，float64 输入/权重时内部 dtype 失配

### 修复（设备无关、dtype 无关）
`pop_code` 与 loss 累积张量全部改用 `spk_out.dtype`：
- `loss.py`: `_population_code()` pop_code、`ce_rate_loss._compute_loss()` 的 pop_code 与 loss 累积张量
- `acc.py`: `_population_code()` pop_code

### 昇腾验证（177 / npu-lizhe 容器，torch 2.14.0a0 + torch_npu 910B）
- Case1 default weight=None popcode → OK（修复前也过，保持兼容）
- Case2 ce_rate_loss float64 权重+输入 → 返回 float64 loss（修复前报 Double 错）
- Case3 ce_count_loss float64 权重+输入 → 返回 float64 loss
- Case4 accuracy_rate float64 popcode → accuracy=1.0 正确类别
- 全部 21 个既有 loss 测试在 NPU 通过，无回归

### PR
- PR #451 fix(population_code): preserve input dtype in population-code helpers — https://github.com/jeshraghian/snntorch/pull/451（Fixes #428, #429）

