# verl-project/verl-omni

昇腾适配贡献记录（B 类跟踪中）。

## PR

| PR | 标题 | 状态 | 验证等级 | 提交日期 |
|----|------|------|----------|----------|
| [#769](https://github.com/verl-project/verl-omni/pull/769) | `[reward] fix: let the whisper_cer scorer select non-CUDA accelerators` | open | 🔴 真机（Ascend 910B2 ×4） | 2026-10-16 |

关联 issue：[#768](https://github.com/verl-project/verl-omni/issues/768)（自建，bug 类）

## 时间线

- **2026-10-16**：head `352b653e` 提交（1 commit / 2 文件 / +155−4）。真机 13 单测过。
- **2026-10-17**：CodeRabbit 4 条 review 处置完 → head **`b3be4cf9`**（2 commits / +225−4，16 单测）。
  - 修 finding ①（`current_accelerator(check_available=True)` + 老 build `TypeError` 兜底）
    与 ④（抽 `_import_torchaudio_functional()` 捕获 `(ImportError, OSError)`）。
  - 答复 finding ②（降采样缺低通）③（重采样长度无上界：8 MiB 体 + `sample_rate=1` ⇒ ≈89 GiB 分配）——
    两条**未改码**，已在 thread 里说明并征求意见。
  - 4 条 bot 线程全部答复，末轮完成（head `5a2860f7`，5 commits / +280−6）。
  - **③ sample_rate：我第一版改错了**——只加 384 kHz 上限，`sample_rate=1` 仍被接受（上限管不住下界），
    且我在评论里**贴出了实测为假的结论**。bot 指出后当场复测确认、**撤回并更正**，
    改为 8000..384000 Hz 区间：8 MiB 体最坏 4.19 M 输出采样（16 MiB）对原先 33.6 G。
    教训：改动生效范围要**对整个取值域跑矩阵**，不能只测自己刚写的那一侧。
  - ② 按 bot 认可的 (a)：`linear_resample` docstring 写明非带限（降采样会混叠、升采样会有镜像），
    未采用 bot 初稿里「alias-free for upsampling」的过宽表述（bot 自己也否了）。
  - 单测 5→19 条；真机（910B2×4）19/19。

## 关键事实（复核用）

- `AGENTS.md` 硬口径：AI 辅助 PR **必须**在描述里写 ①为何不是重复 PR ②跑过的测试命令与结果 ③明确声明使用 AI 辅助；禁止纯 agent PR（提交人须逐行 review 并跑测试）。
  **且明文要求**：agent「不得 push / 开 PR / 标记 ready / 发评论 / 改标签 / 触发 CI，除非用户对该动作明确要求」——违反可自动封禁。
  ⇒ 本仓所有对外动作必须逐次获得用户授权。
- 标题格式（`tests/special_sanity/check_pr_title.py` 为权威源）：`[{module}] {type}: {desc}`，
  modules 白名单含 `reward`，types 含 `fix`。
- `.agents/rules/reward.md`：scorer 由配置选择，**不是**在 `reward_score/__init__.py` 加分支。
- 首贡献者 fork PR 的 workflow 会停在 `action_required`（不产生 check-run），不是失败。
- `__all__` 被上游测试断言为 `["WhisperCERScorer"]`，切勿扩张公开导出。

## CodeRabbit 四条结论（实测，非照抄 bot 措辞）

| # | bot 说法 | 实测 | 处置 |
|---|---------|------|------|
| ① | `current_accelerator()` 只做编译期检查 | **成立**：编译期有 CUDA、运行期无设备的假 torch ⇒ 返回 `cuda:0`，探针一次未调用 | 已修 |
| ② | 降采样缺低通 ⇒ 混叠 | **成立**：48k/12kHz 下采样输出 p-p 仍 1.99 | 答复+征求意见 |
| ③ | `sample_rate` 无上界 | **成立且放大**：8 MiB 体 + `sample_rate=1` ⇒ 目标长度 2.39e10 ≈ 89 GiB | 答复+征求意见 |
| ④ | torchaudio 原生库加载失败抛 `OSError` | **成立**：`torchaudio._extension._load_lib` 文档明写「库找到但加载失败时 as-is 抛出」 | 已修 |

RED 证据：未修代码 + 新测试 ⇒ 2 failed / 14 passed；修后 ⇒ 16 passed（本机与真机一致）。

## 仓库口径

- 上游 `AGENTS.md` 硬口径见上；`.github/`、`AGENTS.md`、`.agents/` 属受保护面，不得改。
- 真机通道：直连 `ssh root@192.168.9.177` → 容器 `npu-lizhe` → `/opt/miniconda/envs/npu/bin/python3`
  （先 `source /opt/ascend/ascend-toolkit/set_env.sh`）。169 无可用 torch_npu，勿用。

## 证据

- [`verification-npu-whisper-cer.md`](verification-npu-whisper-cer.md) — 真机探针 + 单测实际输出
