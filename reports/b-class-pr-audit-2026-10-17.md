# B 类 open PR 处置审计（2026-10-17）

来源：实时 API 全量扫描 68 个 open PR（author:li-lizhe），四个维度：球在谁手里 / 冲突 / CLA / CI / 未回的评论线程。
**不是复述 cron 报告**——cron 的 7 天节流会漏，本次全量不节流。

## 结论：2 件真需要动手，其余为「等对方」或「非我方问题」

### 🔴 1. crewAI #7603 —— 我们加的测试里有一条错断言（我们自己的缺陷）

`lib/crewai/tests/experimental/evaluation/test_experiment_runner.py` 第 237 行（在**我们新增的 33 行块内**，
base 文件只有 209 行、该块从 210 行起）：

```python
assert runner._assert_scores({"a": 3, "b": 7}, 5) is True   # 实际返回 False
```

**实测证据**：取出 head `1ddd0307` 的**真实** `runner.py` 源码执行该真实方法，逐条跑该测试块的全部 11 条断言
⇒ 10 条 ok、**这条 FAIL**（expected dict 非空、actual 标量 ⇒ `all(5>=3, 5>=7)` = False）。
两个独立 bot（coderabbit、cursor）都指向这一处，方向一致。

危害：PR 合入即让该仓测试变红。改法一行：`is True` → `is False`（或改成 `{"a": 3, "b": 4}` 保持 True 的语义）。

### 🟠 2. VoiceStudio #2582 —— 冲突（dirty），可自主 rebase

`mergeable=false`，落后 main 2 个提交。冲突源：`CHANGELOG.md` 在 main 上从 369482 → 373534 字节（别人也改了它）。
另两条 `backend/api/routers/system.py`、`tests/.../test_system_gpu_detection.py` 双方字节数相同、应可干净合。

## ⏳ 等对方（不必动）

| PR | 状态 | 说明 |
|----|------|------|
| docling #4158 | ms=clean | 维护者 cau-git 已于 10-14 **APPROVED**，等合并 |
| chatterbox #554 | ms=blocked | 最后发言者是外人，APPROVED 但非维护者（注册于 approve 前 12 分钟），按 open 处理 |
| LMCache #5776 | ms=blocked | 真人 deng451e 10-16 给了一条 nit（建议别给 in-process 模式加测试）；**我们已在 issue comment 回复**解释覆盖的是 `ret_first_tok` 分支，且该 review 同时给了 APPROVED |
| vllm-ascend #17888 | ms=blocked | CI 红在 `cpu-ut`（`FileExistsError: /tmp/pytest-of-root/.../shared-output`，本 PR 未触及的路径；同轮另一 matrix 项 7741 测试通过）。已评论说明并请求重跑（fork 无 rerun 权限） |
| sglang #40355 | ms=blocked | `pr-gate` 卡在 `Missing required label 'run-ci'`（仓库规定 fork PR 需维护者加标签），已评论请求 |
| triton-ascend #2454 | ms=blocked | 3 个失败全是 **自托管 runner 的容器失败**（annotations：`Executing the custom container implementation failed. Please contact your self hosted runner administrator.`）⇒ 非我方代码问题 |

## 📮 有未回的 bot 评论线程（低优先，可选择性回复）

共 10 个 B 类 PR 存在未回的 bot 线程。已核实其中两条**已过时**（不必回）：

- **whisperX #1469**：Copilot 说「只 catch ImportError 不够」——head `50ab570b` 现在写的是 `except Exception`，已覆盖（正是我在 verl-omni #769 修的同一类问题）。另两条「注释是中文」的指摘也已不成立（`# torchaudio has no Linux aarch64 wheels`，英文）。
- **DeepSpeed #8524/#8525**：codex 的 P1「缺 sign-off trailer」——**实测两个 PR 的 head 提交都有 `Signed-off-by: li-lizhe <147392333@qq.com>`**，author/committer 也都是该邮箱；bot 说的是更早的 commit，已过时。
  另一条 P1「ZenFlow 通信 buffer 应留在加速器」——PR 改的正是 `device='cuda'` → `get_accelerator().current_device_name()`，**就是我们想做的事**，无冲突；但可考虑回一条澄清。

其余待回（gpustack #6338 ×4、vllm-ascend #17864 ×3、crewAI #7603 的 csv_loader BOM ×1、speculators #1196 ×1、VoiceStudio #2582 ×2）多为文档措辞/风格建议。

## 🅰️ A 类（pytorch，只报不动）

| PR | 维度 |
|----|------|
| #195246 | dirty + CI 红 3 项（linux-docs 等） |
| #195261 / #195247 / #195245 | CI 红 1 项（`torchtitan-x-pytorch-test`） |
| #192208 | dirty |

## 📊 全量健康度

- open PR：68；`needs_action`（任一维度命中）：19
- **CLA：全部 success**（`CLA` ×1 / `EasyCLA` ×11 / `license/cla` ×5），无一处失败
- 全程零真人评论（纯等 review）：12 条
- 扫描错误：0

## 方法留痕

- 工具：`our-open-prs-decision-sweep.py`（只看最后真人发言者）+ 自写四维全量扫描（补 CI/CLA/未回线程，因为前者看不到「bot 提了但我没回」——正是 verl-omni #769 那类漏网）
- 只读 GET，全程未 POST/PATCH
