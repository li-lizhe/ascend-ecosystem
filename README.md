# Ascend Ecosystem · 昇腾生态适配

在国产昇腾（Ascend）NPU 上，让优秀的开源软件**开箱即用**，并把适配改动以**设备无关、最小侵入**的方式提交回上游，形成可复现、可推广的技术内容。

## 目标

三个坚持：

1. **设备无关** —— 不写 `if npu:` 硬件特判，统一走 PyTorch 多设备抽象（`torch.accelerator` / `device_type`）。
2. **最小侵入** —— 保留原后端优先路径，只在目标平台不可用时兜底，x86 用户零影响。
3. **先验证后提交** —— 所有改动在真实 910B 环境跑通 E2E 再提 PR，附性能 / 精度数据。

## 已提交 PR

| 分类 | 计数 | 详情 |
|------|------|------|
| ✅ **已合并**（上游合入） | 10 | kornia(2) · snntorch(3) · FunASR · VoiceStudio(2) · ComfyUI LayerStyle · spikingjelly |
| 📡 **跟踪中**（PR 待 review） | 15 | 详见下方 |
| 🔒 已关闭未合入 | 3 | kornia(2) · stable-audio-tools(1) |

详见 **[PRS.md](PRS.md)**（已合入 10 · 跟踪中 15 · 已关闭 3，分表格）。每项目细节见 `projects/<name>/README.md`。

## 规划中

见 **[roadmap.md](roadmap.md)** —— 候选项目将逐一评估 → 适配 → 验证 → 提 PR → 写教程。

## 目录

```
tutorials/   推广教程（带截图，同步发知乎 / CSDN）
projects/    已完成项目的技术摘要与 PR 追踪
shared/      可复用件：去 torchaudio 化模板、checklist
roadmap.md   后续规划
```

## 环境

8× 昇腾 910B2（鲲鹏 ARM aarch64 · openEuler），torch `2.14.0a0`（华为 fork）+ torch_npu `2.14.0` + CANN 9.1。

## 参与

欢迎 issue / PR 提名想适配的项目，或 review 现有 PR。