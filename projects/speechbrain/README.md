# speechbrain — infer_device 只认 CUDA，非 CUDA 加速器被强制 CPU

- **Repo**: speechbrain/speechbrain (11.8k★, 活跃: pushed 5 天内, 近30条 closed PR merge 率 70%, 最近 merge 7 天前) — 通过硬门槛
- **问题来源**: 主动发现（skill「从认领现成 issue 转向主动发现 device 假设」路线；repo 内搜 NPU/infer_device 无任何 issue，属「没人报却实实在在崩在昇腾」的隐式 CUDA-only 假设）
- **根因**: `speechbrain/utils/distributed.py::infer_device()` 用 `torch.cuda.is_available()` 猜设备，非 CUDA 加速器（npu/mps/xpu）一律回退 `cpu`。该函数被 `Brain`（core.py:299）和全部预训练接口（inference/interfaces.py:278）调用——昇腾机器上整个工具链被压到 CPU，多进程还全部挤在 CPU 上。
- **修复**（device 无关，2 行核心改动 + 21 行单测）: 改用 `torch.accelerator.is_available()` / `str(torch.accelerator.current_accelerator())`（PyTorch Multi-Device 官方 API，CUDA 机器行为不变）。坑：`current_accelerator()` 返回 `torch.device` 对象，`+= f":{rank}"` 会 TypeError，必须先 `str()`——昇腾实测第一轮就抓到，已修。附 `test_infer_device` / `test_infer_device_local_rank` 单测。
- **昇腾验证**（910B, torch 2.14.0a0 + torch_npu 2.14.0, 容器 npu-lizhe）:
  - 旧代码在有 NPU 时返回 "cpu"（复现 bug）
  - 新代码返回 "npu"，`Linear(2,2).to("npu")` 前向通过；LOCAL_RANK=1 → "npu:1"
  - 真实 import 验证：最小包结构加载修改后 distributed.py，infer_device() → 'npu' (str)，forward on npu:0
- **分支**: `scan-today/speechbrain` 分支 `accelerator-infer-device`（commit 474268f，base develop）
- **状态**: ✅ 已提交 PR [#3080](https://github.com/speechbrain/speechbrain/pull/3080)（2026-09-02）
- **tracking**: check_prs.py key `speechbrain-PR`
- **备注**: torch>=2.1 而 torch.accelerator 需 2.4+，PR body 已主动提出可加 getattr 降级守卫
