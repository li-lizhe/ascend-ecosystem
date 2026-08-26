# 去 torchaudio 化 · 适配 checklist

在 aarch64 + 华为 torch 环境给 ASR / 语音项目「去 torchaudio 依赖」的通用套路。

## 何时适配

1. `import torchaudio` 是否失败？失败才需要适配（x86 装得上就不动）
2. torchaudio 被用在哪些能力：fbank 特征 / 音频加载 / 重采样 / 训练对齐

## 三步

### 1. fbank / 特征提取

- 优先 `kaldi-native-fbank`（独立 C++，无 torch 依赖，有 manylinux aarch64 wheel）
- 模板：[fbank_kaldi_native_fbank.py](fbank_kaldi_native_fbank.py)（保留 torchaudio 优先路径）
- 调用方只改一处 import：`from torchaudio.compliance.kaldi import fbank` → 你的 shim 路径

### 2. 音频加载

- `torchaudio.load` → `soundfile.read` / ffmpeg 后端（注意采样率重采样）

### 3. 顶层 import

- 顶层 `import torchaudio` → try/except，失败置 `None`
- 目的：保证模块树可被扫描，不拖垮核心推理

## 验证清单

- [ ] `import torchaudio` 确认 ModuleNotFoundError
- [ ] 各调用方 import 不崩
- [ ] fbank 输出 shape 与 torchaudio 一致
- [ ] E2E 推理跑通 + 记录 RTF
- [ ] x86 + 有 torchaudio 环境回归（优先路径仍走 torchaudio，零影响）

## 坑

- 华为 torch 版本号与官方脱钩（`2.14.0a0` vs `2.11`），官方 torchaudio 无匹配 wheel
- 共享容器装包要锁 `numpy==1.26.4`（triton-ascend 依赖），并 `--no-deps`
- 「ffmpeg is not installed. torchaudio is used to load audio」这类是固定提示文本，不代表真用了 torchaudio；看 `load_utils.torchaudio` 是否为 `None`