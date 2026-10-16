# 早 6 点邮件哨兵 · 漏报事故复盘与修复 · 2026-10-16

> 起因：用户 2026-10-16 08:0x 质疑「从昨天到今天我收了好几封真人邮件呢，你怎么说只有一封，你扫描的对吗」。
> 结论：**用户是对的，哨兵漏报。** 06:09 那轮报告「新事件 1（真人 1）」是错的，真实是 **9 条（真人 8）**。
> 漏的是最不该漏的一类：triton-ascend 三个我方 bug issue 的维护者回复（对方在问我们要 CANN 9.1 复现用例）。

## 1. 复核方法与证据（只读邮箱，未标已读、未移动任何邮件）

| 复核项 | 结果 |
|---|---|
| 独立重扫（不用扫描器逻辑，UID SEARCH + UID FETCH 逐封） | 7 天窗 **186 封** GitHub 通知 |
| 扫描器自报 | `文件夹 8 个 | GitHub 邮件 90 封` |
| 差异 | 186 = 90（有效文件夹）+ **96（`Deleted Messages`）**。`Deleted Messages` 是 9-25 清理时 bot 噪音的堆放处，被 `SKIP_BOXES` 有意跳过 ⇒ **这 96 封不是漏报**，扫描器对该文件夹的取舍是正确的 |
| 逐封判定 186 封中的「真人、非 CI」邮件 | 84 封 |
| 其中被扫描器**报出** | 58 封 |
| 其中被**静默丢弃** | **26 封**（其中 9 封是 VoiceStudio CLA issue 的正常通知，属另一条已处理线） |
| **真正有信息量、却完全没进报告** | **17 封** |

## 2. 根因：`parse_subject()` 把 `(Issue #N)` 直接判 None → `skipped` 静默丢弃

`pr_mail_scan.py` 旧逻辑：

```python
if re.search(r"\((?:Issue|Discussion)\s+#\d+\)", rest):
    return None          # ← 这里丢的
```

后果：**维护者直接在我们开的 bug issue 下的回复，永远不会出现在报告里**。
issue 没有 PR review，邮箱里就是 `Re: [repo] 标题 (Issue #N)` ⇒ 被判 None ⇒ `continue` 前只 `skipped += 1`，
报告里连一行都不显示（`skipped` 计数也不在骨架里）。这正是「静默丢弃」的经典形态。

### 被丢弃的 17 封（7 天窗，逐条）

| 时间(CST) | repo#issue | 发件人 | 性质 |
|---|---|---|---|
| 10-15 16:39 | triton-ascend#2529 | Skyminers | **维护者回复：已安排工程师跟进** |
| 10-15 16:44 | triton-ascend#2531 | Skyminers | **维护者问：只在 CANN 9.2 复现吗？请给 CANN 9.1 复现用例** |
| 10-15 16:47 | triton-ascend#2530 | Skyminers | **维护者问：3.5.0 是笔误吗？请给 CANN 9.1 复现用例** |
| 10-14 23:10 | SWivid/F5-TTS#1326 | SWivid | Issue 关闭（completed via #1327） |
| 10-13 14:22 | DiffSynth-Studio#1707 | Artiprocher | Issue 关闭（completed via #1708） |
| 10-13 09:17 | espnet/espnet#6812 | sw005320 | Issue 关闭/回复 |
| 10-13 08:12 | speechbrain#3103 | pplantinga | 新 issue 提及（我方相关） |
| 10-12 12:43 | evalscope#1817 | Yunnglin | `Closing as not planned`（维护者给出理由） |
| 10-11 23:01 | modelscope/twinkle#302 | tastelikefeet | Issue 关闭（completed via #301） |
| 10-11 13:26 | SWivid/F5-TTS#1319 | SWivid | Issue 关闭 |
| 10-10 15:31 | fish-speech#1338 | Whale-Dolphin | Issue 关闭（completed via #1339） |
| 10-09～10-13 | VoiceStudio#2586 ×6 | 多人 | CLA sign-here issue 的评论（已由 CLA 线单独处理） |

**其中 3 封（triton-ascend）是硬信号**：对方把球踢回给我们要复现材料，
按现有哨兵逻辑永远不会被报出 —— 与 docling #4158 藏了 18 天是同一类事故（"维护者最后说话且≥3 天"的「我们欠回复」桶）。

## 3. 修复（已落地并实跑验证）

| 改动 | 文件 | 说明 |
|---|---|---|
| `parse_subject_any()` | `scripts/pr_mail_scan.py` | 同时解析 `pr` / `issue` 两种；旧 `parse_subject()` 保留为 PR-only 薄包装 |
| issue 事件收集 | `scripts/pr_mail_scan.py` | `reason == author`（我方开的）或 `ISSUES.md` 已登记 ⇒ 收作事件，URL 用 `/issues/<n>`，报告标 `(issue)` |
| `load_prs()` 读三文件 | `scripts/pr_mail_scan.py` | 新增解析 `ISSUES.md`，key = `issue:owner/repo#n` |
| `ISSUES.md` 台账 | `scripts/issues_build.py`（新） | API 全量 `author:li-lizhe type:issue state:open` → 重建台账（现有 21 个 open issue） |
| 推送清单 | `scripts/prs_push.py` | `FILES` 加 `ISSUES.md` |
| cron 第一步 | job `c7f5d9f24057` prompt | 串上 `issues_build.py`，报告规则补 issue 说明 |

### 实跑验证（`pr_mail_scan.py --days 7 --dry-run`）

| | 修复前 | 修复后 |
|---|---|---|
| GitHub 邮件 | 90 封 | 90 封（不变） |
| **新事件** | **1 条（真人 1）** | **9 条（真人 8）** |
| 其中 issue 事件 | 0 | **8 条**（SWivid/F5-TTS#1319、#1326、espnet#6807、fish-speech#1338、DiffSynth-Studio#1707、twinkle#302、**triton-ascend#2529/#2530/#2531**） |
| 自审 | 全部文件夹成功 | 全部文件夹成功（无未知区间） |

> 说明：修复后报出的 9 条中，5 条是「issue 已关闭」的补记（属历史，不影响现状），
> **真正需要动作的是 triton-ascend 的 3 条**。另外 `ISSUES.md` 那 21 个 issue 里
> 有 11 个在 7 天窗内没有新邮件 ⇒ 不产生事件（正确）。

## 4. mention 缺口：2026-10-16 已修（用户点名「这个也要修」）

**结论：用户又对了 —— 「mention 被丢」只是那一排洞里的一个。** 顺着修，
同窗口（7 天 90 封）里**被静默丢弃的真人邮件从 18 封降到 1 封**
（剩下 1 封是别人 PR 的关闭通知、与我们无关）。

### 认领口径从 2 条扩到 5 条

| # | 口径 | 修掉的漏报 | 实现 |
|---|---|---|---|
| ① | `reason=author` | 我们自己开的 PR/issue | 原有 |
| ② | `ISSUES.md` 已登记 | 我方 open issue（维护者直接回） | §3 |
| ③ | **粘性线程册命中** | 我方 issue **被关闭后**又来追评 | 新增 `threads_build.py` → `pr_mail_threads.json`（236 条，含已关闭；`author:li-lizhe` ＋ `commenter:li-lizhe` 并集，只增不减、30 天滚动） |
| ④ | **`reason=mention` 且发件人真人** | 别人在 issue/PR 里 @ 我们 | 本次（用户点名） |
| ⑤ | **该线我们评过论**（API 核实） | `reason=comment` 的追评（我们只评过一句、不在任何册子） | 新增 `we_participated()` + `state.participated` 缓存 |

### 每条的实测证据（都在本窗口内）

- **④ mention**（用户点名）：`speechbrain#3103`（pplantinga）、
  `cosdt/pytorch-initial-pr-reviews#1`（KarhouTam）、`vllm-omni#8816`（JoeLoveSally）
  —— 3 封，现已报出并标 `⚠️别人 @ 我们（未登记）`。
- **③ 粘性线程册**：4 封（`evalscope#1817`、`VideoX-Fun#503`、`MinerU#5564`、`tilelang#3380`）
  —— 全是「我们开的 issue 关闭后对方又来追评」。
- **⑤ 我们评过论**：`vllm-omni#8867`（JoeLoveSally：「同意两方案功能等价」——真要看）。
- **踩到并修掉的真 bug**：PR 的普通评论在 `/issues/{n}/comments`，
  `/pulls/{n}/comments` 是 review comment。原先查错路径 ⇒ #8867 有我们 10-14 的评论却判
  False 继续丢。已改两条路径都查。

### 留痕

- 汇总行新增 6 维度：`issue 事件 · ❕别人 @ 我们 · 💬 我们评过 · 粘性线程册命中 · 仍丢弃`
- 末尾打印 `⚠️ 未登记线程 K 个` 清单；cron 要求「仍丢弃 ≠ 0 必须逐条交代」
- cron `c7f5d9f24057` 第一步：`prs_build.py && issues_build.py && threads_build.py && prs_push.py`
- **修复前后：18 封 → 1 封**（§3 那轮修 8 封，本轮再修 9 封）

### 仍未闭合的一处（如实说）

`cosdt/pytorch-initial-pr-reviews#1` 是 KarhouTam 的私人评审仓（我们被 @）。
现在能报出，但它既非我方 PR 也不在 `PRS.md` ⇒ 每轮都会落进「未登记线程」清单。
**这是预期行为**（提醒有人 @ 我们），不是漏报。

## 5. 一句话

用户两次质疑都成立：第一轮发现哨兵把「维护者在我们自己开的 issue 下的回复」整类静默丢弃；
第二轮（mention）发现那只是一排洞里的一个。7 天窗内共 18 封真人邮件被静默丢弃，
现已降到 1 封（一条与我们无关的关闭通知）。事件数 1 → 9（§3）→ 18（§4）。
