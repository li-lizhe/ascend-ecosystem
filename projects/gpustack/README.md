# gpustack/gpustack —— chart 静默丢 worker（PR #6338）

| 项 | 内容 |
|---|---|
| 仓库 | `gpustack/gpustack`（T1 新仓，队列来源 `new_pr_targets.json`） |
| issue | [#6264](https://github.com/gpustack/gpustack/issues/6264)（已有 issue，先认领后提 PR，认领评论 [issuecomment-5995272873](https://github.com/gpustack/gpustack/issues/6264#issuecomment-5995272873)） |
| PR | [**#6338**](https://github.com/gpustack/gpustack/pull/6338) `fix(chart): refuse unsupported worker.gpuVendors names` |
| 分支 | `fix/chart-refuse-unsupported-vendor`（HEAD `18e2a3d` 本地；单 commit） |
| 投递时间 | 2026-10-05 21:18（北京） |
| 规模 | 4 文件 **+108/−8** |

## 根因

`charts/gpustack-chart/values.yaml` 的 `worker.gpuVendors` 填了不在 canonical 列表里的名字（拼错或自造）时：

- `worker-daemonset.yaml` 遍历 `sortedVendors`，非法名被**丢弃** ⇒ 一个 DaemonSet 都不渲染；
- 但 `helm install` 照旧**成功返回**（render 阶段无任何 fail）；
- 若同时开了 CPU DaemonSet，或列表里混了合法 vendor，发布看起来"健康"，实际整类 GPU 节点永远没有 worker；
- 报错信息完全不指向 values 里的拼写问题。

## 改动（4 文件）

| 文件 | 改动 |
|---|---|
| `charts/gpustack-chart/templates/validate.yaml` | +38/−5：新增 guard —— `worker.enabled` 时逐个校验 `worker.gpuVendors`，**读去重前的原始列表**（`sortedVendors` 已把非法名丢掉，正是要抓的对象），非法即 `fail` 并列出全部支持的 vendor 名；同步更新文件头说明 |
| `charts/gpustack-chart/README.md` | +1/−1：`worker.cpuEnabled` 注释补上"两者都为假 ⇒ 无 worker"的说明 |
| `docs/installation/helm.md` | +2/−2：安装文档同步 |
| `tests/charts/test_chart_render.py` | +67/−0：渲染断言回归测试（含本 PR 的三个新场景） |

## 验证（2026-10-05 22:0x 本机复跑，证据见 `verify/`）

环境：`helm v3.16.4`（`oss/_bin/windows-amd64/helm.exe`）+ `.venv_pr`（pytest 9.1.1）。
**所有 helm 命令都必须带 `--set image.tag=dev-test`**，否则该 chart 自身会以 `image.tag is required` 失败（与本次改动无关，第一次跑就踩了）。

修复前 = `HEAD~1` 的 `validate.yaml`；修复后 = 当前 `validate.yaml`：

| 场景 | 修复前 | 修复后 | 证据 |
|---|---|---|---|
| `worker.enabled=true` + `gpuVendors={bogus}` | exit **0**（静默）| exit **1**（指名报错）| `verify/before_bogus.txt` / `verify/after_bogus.txt` |
| `worker.enabled=true` + `gpuVendors={nvidia,bogus}` | exit **0**（只渲染 nvidia）| exit **1** | `verify/before_mixed.txt` / `verify/after_mixed.txt` |
| `worker.enabled=true` + `gpuVendors={nvidia}` | exit 0 | exit 0（无回归）| `verify/before_legal.txt` / `verify/after_legal.txt` |
| `worker.enabled=false` + `gpuVendors={bogus}` | exit 0 | exit 0（不该管就不管）| `verify/before_disabled.txt` / `verify/after_disabled.txt` |

修复后的报错原文（`verify/after_bogus.txt`）：

```
Error: execution error at (gpustack-chart/templates/validate.yaml:74:4): worker.gpuVendors names
unsupported GPU vendor(s): bogus. Supported vendors are: amd, ascend, cambricon, hygon, iluvatar,
metax, mthreads, nvidia, thead. No DaemonSet is rendered for an unsupported name, so the release
would install without a worker for those nodes — fix the spelling or remove the entry.
```

另两项：

- `helm lint charts/gpustack-chart --set image.tag=dev-test` → **1 chart linted, 0 failed**（`verify/helm_lint.txt`）
- `pytest tests/charts/test_chart_render.py -q --noconftest` → **42 passed, 2 xfailed in 118.41s**（`verify/pytest.txt`）

复跑命令：

```bash
export PATH="/c/Users/华为/oss/_bin/windows-amd64:$PATH"      # helm 3.16.4
cd /c/Users/华为/oss/gpustack
helm template t charts/gpustack-chart --set image.tag=dev-test \
  --set worker.enabled=true --set worker.gpuVendors={bogus}
/c/Users/华为/oss/.venv_pr/Scripts/python.exe -m pytest tests/charts/test_chart_render.py -q --noconftest
```

## 未测 / 已知边界（诚实标注）

- **没有**跑真实集群 `helm install` —— 该行为完全在 render 阶段决定，`helm template` 已覆盖；
- `higress-core` / `gpustack-operator` 子 chart 按其钉定版本渲染，内部未改；
- 本机 pytest 用了 `--noconftest`：仓库根 `conftest.py` 会 import `gpustack.config` → 需要未安装的 `gpustack_runtime`；chart 渲染测试不依赖那些 fixture（首次不带 `--noconftest` 时 import 失败，见下"踩坑"）。

## 门禁状态（2026-10-05 22:1x 实测）

- check-runs：`build (linux/arm64)` ✅、`build (linux/amd64)` ✅、`review / review` ✅、`metadata` ✅、`linux-build (3.12)` ✅；`chart` / `merge` = skipped；
- 无 CLA/DCO 标签或 bot 报错（该仓未见 CLA 门）；
- 无 `mergeable_state` 阻塞项记录（尚未取）。

## 踩坑记录（下次少走）

1. `helm template/lint` 不带 `--set image.tag=...` 一定失败，报的是 `server-statefulset.yaml` 的 `image.tag is required` —— 别误判成自己的改动弄坏了 chart。
2. `helm lint` 不带 `image.tag` 时报的是 `templates/server-statefulset.yaml: unable to parse YAML`（空 tag 渲染出坏 YAML），同样与改动无关。
3. pytest 必须 `--noconftest`（见上）；`-q` 下 118s，属正常（每个用例都在跑 helm）。

## 证据文件

- `verify/before_*.txt`、`verify/after_*.txt` —— 四场景 × 前后 的 helm 输出与 exit code（渲染成功的大文件已截断为前 25 行，保留 exit code 与错误原文）
- `verify/helm_lint.txt`、`verify/pytest.txt` —— lint 与回归测试原始输出
- `PR-6338.patch` —— 该 PR 的完整 patch（`Accept: application/vnd.github.patch`）
