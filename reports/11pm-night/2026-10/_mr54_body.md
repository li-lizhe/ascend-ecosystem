### 问题（对应 #14）

`scripts/run_tests.py` 会记录开源报告生成器的退出码，但只把失败打到 stderr：

```python
gen_rc = generate_opensource_report(paths.results_json, paths.opensource)
if gen_rc != 0:
    print(f"[test] opensource report failed rc={gen_rc}", file=sys.stderr)
```

`main()` 的最终状态只看测试用例失败数（以及 `--opensource-report` 的目标文件是否**存在**）。当目标路径上还留着上一次的报告文件时，「本次生成失败」和「本次生成成功」在退出码上无法区分：runner 打印 `fail=0`、退出码 0，自动化会把上一次的陈旧报告当成本次结果。

`finalize_reports()` 的返回值是 `None`，所以调用点拿不到生成器的退出码。

### 复现（Host，无需 NPU）

让 `--opensource-report` 指向一个已存在且本次写不进去的报告文件：

```bash
python3 scripts/run_tests.py --suites= --opensource-report=<existing-report-path>
```

原版：stderr 打印 `[test] opensource report failed rc=<非零>`，但退出码为 `0`，旧报告文件原样保留。

### 修改

`finalize_reports()` 返回生成器退出码（未请求该报告时返回 `0`），`main()` 把它并入最终退出码。这样「本次生成失败」一定表现为非零退出码，与「报告文件是否存在」无关。

报告写出顺序、报告内容、套件编排、`--report` / `--results-json` 的行为均不变。

### 验证

**1. 真实端到端（🔴 aarch64 主机，非 root 用户，真实不可写目标）**

环境：aarch64 / openEuler，Python 3.11.6。用 `setpriv --reuid=65534` 以普通用户运行生产脚本，目标报告文件由 root 持有且只读（`444`），即本次写入必然失败；目录里预置一份「上一次的报告」。

| | 上游版 | 补丁版 |
|---|---|---|
| 退出码 | **0** ❌ | **1** ✅ |
| stderr | `opensource report failed rc=1` | 同左 |
| 旧报告文件内容 | 原样保留（未被改写/删除） | 原样保留 |
| stdout 末行 | `pass=0 fail=0 skip=0` | 同左 |

对照（同一台机器）：目标改成可写路径时，上游版与补丁版都是退出码 `0` 且真正写出了报告 —— 修法没有影响正常路径。

**2. 回归用例（新增 `tests/host/test_run_tests_report_generation.py`）**

| 用例 | 上游版 | 补丁版 |
|---|---|---|
| 旧报告存在 + 生成失败 → 非零退出码 | **FAILED**（`0 == 0`） | **passed** |
| 生成成功 + 报告落盘 → 仍为 0 | passed | passed |
| 返回 0 但未落盘 → 非零退出码 | passed | passed |

上游版下 `1 failed, 2 passed`（RED 落在本修复点上），补丁版 `3 passed`。用例只 mock `generate_opensource_report`，跑的是仓库里真实的 `main()` / `finalize_reports()` 退出码路径。

**未验证的部分**：用例与端到端都在 Host 上完成，没有在真机 NPU 上跑整套 `-u`；本缺陷不涉及设备路径，设备侧行为未做验证。`tests/host` 目前未被 `.gitcode/workflows/llt_action.yml` 收集（该 workflow 只跑 `tests/triton` 与 `tests/composite`），本次未改动 workflow 文件；若希望这两个用例进门禁，可以另行加一个 `pytest tests/host` 步骤。

Fixes #14

Signed-off-by: li-lizhe <147392333@qq.com>
