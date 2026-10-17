# modelscope/FunASR · 昇腾 910B 适配

达摩院语音识别工具包 [FunASR](https://github.com/modelscope/FunASR) 在昇腾 910B 上「零 torchaudio 依赖」跑通。

## 状态

- ✅ **#3526 已合并**（2026-08-26，by LauraGPT）—— 任务首个成功合入上游的 PR（去 torchaudio 硬依赖）。
- 📡 **#3771 跟踪中**（分布式训练设备无关化；已按 review 收窄到 Ascend 路径，见下）。

## PR #3526（已合入）— 三招去 torchaudio

1. **fbank 特征** → `kaldi-native-fbank` 兜底（新增 shim，保留 torchaudio 优先路径，x86 零影响）
2. **音频加载 / 重采样** → `soundfile`/`librosa` 兜底 + try/except
3. **次要模型 / 数据集顶层 import** → try/except 可选化 + 统一 `torchaudio_compat` guard

问题：FunASR 硬依赖 torchaudio；昇腾 aarch64 + 华为 torch（`2.14.0a0`）无匹配 wheel ⇒ `import funasr` 即崩。关联上游 issue #3523。

### Review 反馈与修复（LauraGPT, CHANGES_REQUESTED）

| 反馈 | 修复 |
| --- | --- |
| kaldi-native-fbank 未声明依赖，干净环境 import 仍崩 | 加 optional `knf` extra；`fbank()` 调用时无后端才报可操作 ImportError |
| shim `**kwargs` 静默吞参（如 `channel`） | 显式处理 `channel`；`subtract_mean`/`min_duration`/VTLN/`blackman_coeff` 显式 NotImplementedError |
| `forced_align` 宽 except 吞缺失依赖、静默返回空 | 新增共享 guard，依赖缺失时传播 ImportError |
| 未测「torchaudio 完全缺席」环境 | 新增 `tests/test_torchaudio_optional.py` 回归测试 |

验证：8× 昇腾 910B2，torch `2.14.0a0+git69231fe`，torch_npu `2.14.0+gitee7bc39`；paraformer-large 70.47s 音频 → 1.15s 推理，**RTF ≈ 0.0164**（约 61× 实时）。

---

## PR #3771（跟踪中）— 分布式训练绑定到活跃加速器

`funasr/bin/train.py`、`train_ds.py`、`funasr/train_utils/trainer_ds.py` 原本全是 CUDA-only 调用
（`torch.cuda.set_device` / `model.cuda()` / `backend="nccl"` / 只在 `device.type=="cuda"` 时清缓存）
⇒ 无 CUDA 的 build（如昇腾）**分布式根本起不来**。

新增 `funasr/train_utils/device_funcs.py`：`get_accelerator_device_type()`、
`accelerator_device()` / `set_accelerator_device()`、`get_default_dist_backend()`、
`clear_accelerator_cache()`（无新依赖，无 `if npu:` 分支）。

### Review 过程（两轮 CHANGES_REQUESTED → 收窄）

| 轮 | 维护者意见 | 我方处置 |
| --- | --- | --- |
| 1（10-11） | `get_default_dist_backend()` 对非 NPU 一律返回 `nccl`，XPU 应走 XCCL | 10-12 修好（head `da0e18cd`），按加速器解析 npu→hccl / xpu→xccl（老 build 回退 `ccl`） |
| 2（10-12） | CUDA 侧已在真 H100 跑通；**merge gate = exact-head Intel XPU 2-rank XCCL 真机证据** | 我方**无 XPU 硬件** ⇒ 10-13 回复两条路待用户拍板 |
| 拍板（10-17） | 用户选 **②收窄到 Ascend 路径、XPU 留 follow-up issue** | **head `0a336ba5`**：`_ACCELERATOR_DIST_BACKENDS` 去掉 `"xpu"` ⇒ XPU 回到 PR 前原值 `nccl`（零行为变化）；XPU 另开 **#3777** |

收窄口径（对外已说明）：我方不具备 XPU 硬件 ⇒ XPU 臂是本 PR 唯一无真机证据的运行路径 ⇒
收窄后**本 PR 仍改动的每条运行路径都有真机证据**，符合仓库硬件验证要求。

### 最终 head `0a336ba5` 证据（🔴 真机，exact head）

- 环境：177 → 容器 `npu-lizhe`，Ascend 910B2 ×4，`torch 2.15.0.dev20260917+cpu` / `torch_npu 2.15.0.dev20260917+gitec69335`
- 2-rank `torchrun`：rank0→`npu:0` / rank1→`npu:1`，`device_type=npu`、`backend=hccl`，
  all_reduce 和 `1.0`，代表训练步 loss 两 rank 同为 `0.835605`（含 fwd+bwd+optimizer.step）
- epoch 末缓存释放：reserved `291504128 → 2097152`；`clear_accelerator_cache(torch.device("cpu"))` 为 no-op
- 单测 `tests/test_distributed_device_setup.py`：**8/8 OK**（本机与真机一致）

### 关联

- follow-up issue：[**#3777**](https://github.com/modelscope/FunASR/issues/3777)（XPU/XCCL 选择未验证，需 XPU 硬件；含修法与所需证据）
- PR 评论（收窄说明）：https://github.com/modelscope/FunASR/pull/3771#issuecomment-6228134947

---

## 关联（历史）

- 教程：[FunASR 在昇腾 910B 上零 torchaudio 跑通](../tutorials/funasr-on-ascend-910b/README.md)
- 可复用件：[fbank shim](../shared/fbank_kaldi_native_fbank.py)、[去 torchaudio checklist](../shared/torchaudio-free-checklist.md)
