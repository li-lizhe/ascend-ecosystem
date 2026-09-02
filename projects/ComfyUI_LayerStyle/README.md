# ComfyUI_LayerStyle — 硬编码 CUDA 检测，非 CUDA 加速器节点静默回退 CPU

- **Repo**: chflame163/ComfyUI_LayerStyle (3.1k★, 活跃: pushed 15 天内, 近30条 closed PR merge 率 90%, 最近 merge 32 天前) — 通过硬门槛
- **问题来源**: 主动发现（repo 内无 NPU/device 相关 issue/PR；RMBG/vitmatte 等路径 `"cuda" if torch.cuda.is_available() else "cpu"` 硬编码）
- **根因**: 多处设备选择硬编码 CUDA 探测而非用仓库已 import 的 `comfy.model_management`（ComfyUI 官方 device 抽象，master 已原生支持 Ascend NPU：`get_torch_device()` 返回 `torch.device("npu", i)`）。涉及 `imagefunc.py` 的 load_RMBG_model/RMBG/vitmatte/UformGen2QwenChat/clear_memory 及 `blendmodes.py` 两个 HSV 转换。昇腾上这些节点全部静默跑 CPU（.cuda() 分支则崩）。
- **修复**（+17/-12 行）: 统一改用 `comfy.model_management.get_torch_device()`；RMBG 输入跟随 (lru_cache) 模型自身设备；vitmatte 尊重显式 cpu、其余走 ComfyUI 默认设备；clear_memory 增加 `torch.accelerator.empty_cache()` 非 CUDA 加速器分支。
- **昇腾验证**（910B, torch 2.14.0a0 + torch_npu 2.14.0, ComfyUI master model_management 实现）:
  - `get_torch_device()` → `torch.device("npu", 0)`
  - conv2d 前向 + RMBG 式 model/input 流程在 npu:0 正常
  - `torch.accelerator.empty_cache()` 可调用
- **分支**: `scan-today/ComfyUI_LayerStyle` 分支 `comfy-device-selection`（commit 6555d35）
- **状态**: ✅ 已提交 PR [#609](https://github.com/chflame163/ComfyUI_LayerStyle/pull/609)（2026-09-02）
- **tracking**: check_prs.py key `layerstyle-PR`
