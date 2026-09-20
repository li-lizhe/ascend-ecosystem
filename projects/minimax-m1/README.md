# MiniMax-M1 昇腾适配

## 问题

`main.py` 示例脚本将 tokenizer 输出强制 `.to("cuda")`，在 CPU 或 Ascend NPU 等无 CUDA 环境下直接报错，用户无法体验模型。

## 修复

PR #43：用 `torch.cuda.is_available()` 选择目标设备，CUDA 可用走 cuda，否则走 cpu。

## 验证

- 在 CPU-only 环境运行脚本不再因 `.to("cuda")` 崩溃，可继续进入 device_map 加载阶段。
- 未在 NPU 真机完整跑通生成流程（模型较大，需多卡环境）。
