# DiffSynth-Studio（modelscope）WanToDance 音乐编码器硬编码 `device='cuda'` — NPU 验证记录

> 归档：昇腾生态适配 `ascend-eco-repo/projects/DiffSynth-Studio/`；非 PyTorch 主仓，**不放入** `mindlog/log` 的 `特性解耦L2/`。
> PR: https://github.com/modelscope/DiffSynth-Studio/pull/1708 · 自建 issue: https://github.com/modelscope/DiffSynth-Studio/issues/1707
> 来源：2026-09-23 晚 21 点探新流水线（**选型驱动扫描**，非 issue 认领）。同轮另一目标见 [`../timm/`](../timm/)。

## 1. 定位

`diffsynth/models/wan_video_dit.py:462`（`WanModel.__init__` 内，受
`wantodance_enable_global / dynamicfps / unimodel` 门控）

```python
                self.music_encoder.append(
                    WanToDanceMusicEncoderLayer(
                        d_model=latent_dim, nhead=nhead, dim_feedforward=ff_size,
                        dropout=dropout, activation=activation,
                        batch_first=True, rotary=rotary,
                        device='cuda',          # ← 硬编码
                    )
                )
```

`diffsynth/models/wantodance.py:156` 把 device 透传给 `nn.MultiheadAttention(..., device=device)`，
即**构造期**就在 CUDA 上分配参数。同 block 里 `nn.Linear` / `nn.Sequential` 都不传 device（交给外层 `.to()`），
项目还自带 `diffsynth/core/device/npu_compatible_device.py`（get_device_type/get_torch_device/hccl），
所以这行是漏网硬编码，不是设计。

## 2. 真机复现（修复前）

投递真实 `diffsynth/models/wantodance.py`（einops 用 `pip install einops --no-deps` 装，避免动 numpy/scipy）：

```
[env] 2.15.0.dev20260917+cpu True
[CRASH] AssertionError Torch not compiled with CUDA enabled
```

## 3. 修复后

去掉 `device='cuda',`（仅 −1 行）：

```
[sig] (self, src: torch.Tensor, src_mask=None, src_key_padding_mask=None)
[FIX-OK] out device= npu:0 shape= (2, 8, 256) sum= -0.5741
[FIX-OK] in_proj_weight on npu:0
```

## 4. 诚实边界

- 未跑端到端 WanToDance 视频生成（需权重 + 整条 pipeline）；验证覆盖「模块构造 + 单次 NPU forward」。
- CUDA 行为不变：模块无 device 构造、由调用方搬到目标设备 —— 这正是 CUDA 上今天的行为。

## 5. 真机环境（169）

```
服务器   root@192.168.9.169   （ssh -i C:\Users\华为\.ssh\id_ed25519）
容器     npu-lerobot
python   /opt/miniconda/envs/npu/bin/python
CANN     source /usr/local/Ascend/ascend-toolkit/set_env.sh
torch    2.15.0.dev20260917+cpu
torch_npu 2.15.0.dev20260917+gitec69335
NPU      8 × Ascend910B4（torch.npu.is_available()=True, device_count()=8）
投递方式 cat pkg.tgz | ssh ... "docker exec -i npu-lerobot bash -lc '...'"
```

## 6. 本轮踩坑（通用，另一目标同样适用）

1. **stdin 被吃掉**：`cat a.py b.py | ssh ... "bash -lc 'cat > b.py'"` 会把**两个文件**都灌进 b.py。多文件一律打成 tgz 再管道投递。
2. **脚本内 `sys.path` 写死**：写死后改投到新目录仍加载旧文件 → 修复后现象不变、差点误判修复无效。
   改成 `os.path.dirname(os.path.abspath(__file__))`。
3. **多租户 AICore 争用**：首次带 forward 的脚本 300s 超时（假 hang）。加 `NPU_AUTOTUNE_MAX_CONFIGS=1` + `timeout`，
   并把崩溃复现与 forward 拆成两段后正常。
4. **仓库改名核对**：查重前先 `GET /repos/<o>/<r>` 核 `full_name`（同轮 timm 的教训：能拉到源码 ≠ 仓库名还对）。
5. **时间戳**：本机时钟比容器快约 233s，`tar xzf` 打印 `time stamp ... in the future` 警告，不影响解包，可忽略。

## 7. 后续可挖（本轮扫描所得，未提交）

- `diffsynth/models/yue2_vae.py:412` `device = "cuda" if torch.cuda.is_available() else "cpu"`
  （NPU 上静默退 CPU，应改用项目自带 `get_device_type()`）
- `diffsynth/utils/dequantizer`、`diffsynth/utils/demucs` 的 `device="cuda"` 默认参数

## 8. 提交动作

| 项目 | issue | PR | 分支 | diff | 验证等级 |
|------|-------|----|------|------|---------|
| modelscope/DiffSynth-Studio | #1707 | [#1708](https://github.com/modelscope/DiffSynth-Studio/pull/1708) | `fix/wantodance-music-encoder-device` | +0/−1 | 🔴 真机 910B4 |

提交流程：fork（API）→ 上游 main sha 建分支 → `PUT contents`（base64 走临时文件，规避 Windows 32K 命令行上限）→
`POST pulls`（head 必须 `li-lizhe:<branch>`）→ 回读 PR 校验 diff。PR 均 `state=open`，无 bot 关闭、无 CLA 阻塞。
**注意：本项目 PR 尚未纳入 `PRS.md` 跟踪表。**
