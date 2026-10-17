# 23:00 岗 8 个产出的「真人 review」与「红 CI」核查 · 2026-10-17

实时 API 逐个回读（GitHub reviews/comments/check-runs/annotations/raw logs；GitCode pulls+comments）。

## 一、真人 review：只有 1 个

| 产出 | 真人 review | 说明 |
|---|---|---|
| !725 MindIE-SD | ✅ **有，已合入** | 4 位真人评论（`kryocode`/`sirius2alpha`/`ZhuanJi_`/`weixin_44144262`，10-12），集齐 `lgtm + approved + keeper_approved` 后 10-16 合入 |
| !1103 msprobe | ✅ **有真人 review** | reviewer `ylw1234` 10-16 提 2 条检视意见，我方已采纳并回推（head `77dc25d`） |
| #17888 vllm-ascend | ❌ 0 真人 | 仅 `gemini-code-assist[bot]` 1 条 bot review；唯一评论是我方自己（10-14） |
| #2454 triton-ascend | ❌ 0 真人 | 连 bot review 都没有；唯一评论是我方自己（10-08） |
| #8189 verl | ❌ 0 真人 | **0 review、0 评论、0 check-run**（一直没人碰） |
| !53 ops-rand | ❌ 0 真人 | 仅我方自己 1 条 |
| !1145 MindIE-Motor | ❌ 0 真人 | 仅我方自己 2 条 |
| !1108 msprobe | ❌ 0 真人 | 仅我方自己 1 条 |

**⇒ 8 个里只有 2 个拿到真人 review（!725 已闭环；!1103 待我再回一轮）。**

## 二、红 CI：3 个 GitHub 产出需要处理，逐条定位

### 1. `vllm-ascend` #17888 — 唯一「真·测试失败」，但是**既有 flaky 测试**，非我方代码

**失败点**：`cpu-ut` 阶段
```
FAILED tests/ut/_tools/test_build_cache.py::test_parallel_actions_have_exact_artifact_ownership
FileExistsError: [Errno 17] File exists: '/tmp/pytest-of-root/pytest-0/.../shared-output'
===== 1 failed, 7741 passed, 67 skipped =====
```

- 我方 diff **只有** `csrc/build_batch_invariant_ops.sh`（+18/−1），与被测的 `csrc/scripts/build_cache.py` **无关**。
- 该失败是**测试自身用固定路径 `/tmp/.../shared-output` 导致的并行冲突**（两次并存 ⇒ `FileExistsError`）。
- `ci-gate` 红是**连带的**：annotation 原文「`cpu-ut` did not succeed (result: failure)」。
- 判定：**非我方 bug，属仓库既有 flaky**。

### 2. `triton-ascend` #2454 — **自托管 runner 基础设施故障**

3 个失败 job 的 annotation 全是同一句：
```
Executing the custom container implementation failed.
Please contact your self hosted runner administrator.
```
明细：
- `Build on Ubuntu 22.04 / ARM64`：脚本步骤挂在 `PyYAML<=6.0.1,>=5.4.0` —— **装不到（No matching distribution）**，即镜像/索引不可达，非代码问题。
- `integration-tests-ascend`：容器实现起不来。
- 旁证：同仓他人 PR 同样大面积红（!2612 红 5 项、!2596 红 4 项、!2589 红 4 项，均为同一 `integration-tests-ascend`）。
- 我方 diff 只有 Dockerfile/llvm-build.yml/patch 三处，**与 LLVM 构建脚本无关**。

### 3. `verl` #8189 — **零 check-run**（CI 从未跑）

- 该 PR 从 10-10 至今 `check-runs = 0`：维护者未触发任何 CI（该仓需维护者加标签/跑 `run-ci`）。
- `mergeable_state = blocked`，0 真人 review、0 评论 ⇒ **完全静止，等维护者**。

### 4. GitCode msprobe !1103 / !1108 — `ci-pipeline-failed`

见 `reports/11pm-night/2026-10/2026-10-17_check.md`：仓库级系统性（30 个 open MR 中 9 个同红），
本地按 CI 等价参数复跑 stage-1 三件套与 master 逐项一致 ⇒ 不能归因我方；
GitCode 无 CI 日志 API，无法定位根因。

## 三、可用的重跑手段（已确认存在）

| 仓 | 手段 |
|---|---|
| vllm-ascend | 有 `/rerun` slash 命令工作流（`.github/workflows/pr_rerun_command.yml`）+ Slash Command Dispatch |
| triton-ascend | 有 `Rebuild / Retry Tasks`（`.github/workflows/rebuild-tasks.yml`） |
| msprobe（GitCode） | 仓内机器人 `compile` 评论命令（我方 10-16 已用过） |
| verl | 需维护者触发（我方无权） |

## 四、建议动作（待拍板）

1. **#17888**：发 `/rerun` 重跑 `cpu-ut`（flaky 大概率转绿，转绿即 `ci-gate` 一并绿）。
2. **#2454**：`Rebuild / Retry Tasks` 重试一次；若仍挂 `PyYAML`/容器故障，即为对方 runner 长期问题，只能等（不影响我方 diff 评审）。
3. **#8189**：无动作可做（等维护者）。若你同意，我可在 PR 下留一条简短 ping 说明已等待 7 天。
4. **msprobe !1103/!1108**：发 `compile` 重跑一次；同时修 !1108 测试文件末尾缺换行（1 字节）。

**注意**：上述 1/2/4 都是在**我们自己的 PR** 上做自助动作（重跑/改自己提交的字节），符合既有授权口径；若要对外发言（ping 维护者）需先给你过目草稿。
