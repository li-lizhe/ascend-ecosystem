# B 类 open PR 处置审计（2026-10-17）

来源：实时 API 全量扫描 68 个 open PR（author:li-lizhe），四个维度：球在谁手里 / 冲突 / CLA / CI / 未回的评论线程。
**不是复述 cron 报告**——cron 的 7 天节流会漏，本次全量不节流。

## 结论：2 件真需要动手，其余为「等对方」或「非我方问题」

### 🔴 1. crewAI #7603 — 我们自己加的测试里有一条断言是错的（已修）

`lib/crewai/tests/experimental/evaluation/test_experiment_runner.py` 第 237 行
（在**本 PR 新增的 33 行里**；该文件原 209 行）：

```python
assert runner._assert_scores({"a": 3, "b": 7}, 5) is True   # 实际返回 False
```

`_assert_scores` 的规则是 actual 必须 >= expected 中每个值，`5 >= 7` 为假。
两个 review bot（coderabbit、cursor）都指向这一行。

**验证方式（可复现）**：从 PR head 拉真实
`lib/crewai/src/crewai/experimental/evaluation/experiment/runner.py`，抽出
`_assert_scores` 绑定到实例，再**逐条执行测试块里的 assertion**：
- 原版：13 条中 **1 条失败**（就是第 237 行）→ RED 确认
- 修正后：**0 条失败** → GREEN

**处置**：改成 `is False`，一行。head `e1af20e0`，CI **4/4 success**。
（初版我多加了两条边界断言，其中 `({"a":3,"b":7}, 7) is False` 本身也错——`7 >= 7` 为真——
已在推送前自查发现并改为最小单行修正。）

### 🟠 2. VoiceStudio #2582 — rebase 冲突（已解决）

`mergeable=false`，落后 main **131 个提交**。

**冲突根因**：本分支的 `CHANGELOG.md` 曾被污染成**别的项目（SpikingJelly）的变更日志**
（commit `c162e095` 的 diff 是 `# 变更日志 | Changelog` + "All notable changes to SpikingJelly"）。
这是本 PR 唯一冲突文件；另两个文件可干净 rebase。

**处置**：rebase 到当前 `origin/main@481cf4c4`，CHANGELOG 取上游版本 + 只补我方那一行
`- Settings → System reports an Ascend NPU host's device name and VRAM … (#2582)`（放在 `[Unreleased] → ### Fixed` 下）；
第二个 commit（纯 changelog 恢复件）内容已归并，跳过。
- head `128cf3bc`，**1 commit**（原 2）、3 文件 `+151/−15`
- **`mergeable: true`**（冲突消除），`mergeable_state: blocked`（等 review / CI）
- `backend/api/routers/system.py`（68546B）与 `tests/.../test_system_gpu_detection.py`（5118B）
  **与改前 PR head 逐字节一致**——只动了 CHANGELOG
- 全部 LF（`\r` = 0）

## 其余不用动

| PR | 状态 | 说明 |
|----|------|------|
| docling #4158 | ✅ 维护者已 APPROVED（10-14） | 等合并 |
| LMCache #5776 | 真人 nit 已回复 | 同轮 review 给了 APPROVED |
| vllm-ascend #17888 | CI 红在 `cpu-ut` 的 `/tmp/.../shared-output` | 非本 PR 路径；同轮另项 7741 测试通过；已评论+请求重跑（fork 无重跑权限） |
| sglang #40355 | 等维护者加 `run-ci` 标签 | 已请求 |
| triton-ascend #2454 | 3 个失败 | 全是**对方自托管 runner 容器起不来**（annotations 原文「请联系你的自托管 runner 管理员」），非我方代码 |
| whisperX #1469 | Copilot 称「只 catch ImportError」 | 已过时：代码现为 `except Exception` |
| DeepSpeed #8524/#8525 | codex 称「缺 sign-off」 | 已过时：**实测两个 head 提交都带 `Signed-off-by` 且邮箱正确** |

## 健康度

- CLA：**全部 success**（EasyCLA 11 / license/cla 5 / CLA 1），零失败
- 12 条 PR 自投出起零真人评论（纯等 review）
- 扫描 0 错误

## A 类（pytorch，按规矩只报不动）

#195246 脏 + CI 红 3 项；#195245 / #195247 / #195261 CI 红 1 项；#192208 脏。
