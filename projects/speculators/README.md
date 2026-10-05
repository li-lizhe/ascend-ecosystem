# vllm-project/speculators —— render endpoint 挂掉时静默丢数据（PR #1196）

| 项 | 内容 |
|---|---|
| 仓库 | `vllm-project/speculators`（T1 新仓，队列来源 `new_pr_targets.json`） |
| issue | [#1159](https://github.com/vllm-project/speculators/issues/1159)（已有 issue，先认领后提 PR，认领评论 [issuecomment-5995407341](https://github.com/vllm-project/speculators/issues/1159#issuecomment-5995407341)） |
| PR | [**#1196**](https://github.com/vllm-project/speculators/pull/1196) `fix(data): abort dataset build when the render endpoint fails` |
| 分支 | `fix/render-endpoint-failure-aborts-build`（HEAD `26bcc2c` 本地；单 commit） |
| 投递时间 | 2026-10-05 21:26（北京） |
| 规模 | 3 文件 **+101/−3** |

## 根因

`prepare_data` 期间 render server 挂掉（或 `--render-endpoint` 指到不再应答的地址）时：

- `_render_conversation_rows` 里一个**宽 `except Exception`** 把每次失败都当成"这条对话没有可训练行"吞掉；
- 于是整个 run **正常结束**，返回一个**静默缺失"首个失败点之后全部对话"**的训练集；
- 唯一的聚合告警文案只说 assistant turn / 模板 / 截断，**完全不提 endpoint**。

即：构建产物看起来成功，实际数据大面积缺失 —— 属于"静默错误数据"。

## 改动（3 文件）

| 文件 | 改动 |
|---|---|
| `src/speculators/data_generation/render_client.py` | +21/−2：新增 `RenderEndpointError(RenderError)`，标记"影响**所有**对话"的失败（连接/超时 `httpx.TransportError`、重试耗尽的非 200）|
| `src/speculators/data_generation/preprocessing.py` | +10/−1：`_render_conversation_rows` 在宽 except **之前** re-raise `RenderEndpointError` ⇒ 端点挂了**直接中止**构建；对话自身级失败（模板不稳定、对话畸形）保持原有 skip-and-continue |
| `tests/integration/datagen/test_render_boundary.py` | +70/−0：4 个 endpoint 边界回归测试 |

## 验证（2026-10-05 22:0x 本机复跑，红/绿对照，证据见 `verify/`）

环境：`.venv_pr`（pytest 9.1.1 / httpx 0.28.1 / datasets 2.21 / transformers 5.18 / torch 2.8.0+cpu），
`openai` 不在该环境 ⇒ 用桩补（`verify/` 里留了 `fcntl.py`、`hs_connectors.py` 两个桩，`openai` 桩复用 `oss/_spt/stubs/openai`）。

| 源码版本 | 命令 | 结果 | 证据 |
|---|---|---|---|
| 修复后 `26bcc2c` | `pytest tests/integration/datagen/test_render_boundary.py -q --noconftest` | **20 passed** | `verify/after_pytest.txt` |
| 修复前 `1a28ebd`（父提交，用 git worktree 取源码；同一份测试文件拷进去） | 同上 | **4 failed, 16 passed** | `verify/before_pytest.txt` |

修复前的 4 个失败即本 PR 要修的行为（原文摘录）：

```
E  AttributeError: module 'speculators.data_generation.render_client' has no attribute 'RenderEndpointError'
FAILED ...::test_render_conversation_transport_error_is_an_endpoint_error
FAILED ...::test_render_conversation_5xx_is_an_endpoint_error
FAILED ...::test_render_conversation_rows_reraises_an_endpoint_failure
FAILED ...::test_build_aborts_when_the_render_endpoint_fails
```

复跑命令：

```bash
PY="/c/Users/华为/oss/.venv_pr/Scripts/python.exe"
S="$LOCALAPPDATA/Temp/spec_stubs"            # openai 桩(拷自 oss/_spt/stubs) + fcntl.py/hs_connectors.py(本目录 verify/ 内)
export PYTHONPATH="C:/Users/华为/oss/speculators/src;$S"
cd /c/Users/华为/oss/speculators && $PY -m pytest \
  tests/integration/datagen/test_render_boundary.py -q --noconftest --override-ini addopts=
# 修复前：git worktree add <tmp> 1a28ebd，再把同一份测试文件拷进 <tmp>/tests/integration/datagen/ 后重跑
```

## 未测 / 已知边界（诚实标注）

- **没有**跑真实 vLLM endpoint（`tests/e2e` 全未跑）；本机是桩驱动；
- 只端到端覆盖了**连接失败**路径；**5xx** 只在 client 层用单测覆盖（没有真起一个会 5xx 的 server）；
- 改动是纯 Python 控制流，不碰张量/设备；`--noconftest` 是因为仓库 `tests/conftest.py` 会 import `tests.e2e.utils`（需要 loguru 等 e2e 依赖），与本次改动无关。

## 门禁状态（2026-10-05 22:1x 实测）

- check-runs：`DCO` ✅、`Summary` ✅；`Mergify Merge Protections` = **failure**，读其原始 output 后确认是
  `waiting on 👀 reviews`（`Require approval from approved reviewers list`）—— **正常的"等 review"门，不是缺陷**；
- combined status：`success`（`docs/readthedocs.org:vllm-speculators` ✅、`CodeRabbit` ✅）；
- 无 CLA 标签。

## 踩坑记录（下次少走）

1. `fcntl` 是 POSIX-only，Windows 上 `vllm_client.py` import 期就炸 ⇒ 本地跑必须补 `verify/fcntl.py` 桩（no-op flock）。
2. `hs_connectors` 是可选 extra；`speculators/__init__` 会一路 import 到 `train/data.py` ⇒ 必须补 `verify/hs_connectors.py` 桩，否则 collection 就失败。
3. `importlib.metadata` 找不到 `speculators` 包元数据 ⇒ 需要 `_spt/stubs/speculators-0.4.0.dist-info` 这类元数据桩。
4. 仓库 `tests/conftest.py` 会拉 e2e 依赖 ⇒ 跑这一支用 `--noconftest` 最省事。

## 证据文件

- `verify/after_pytest.txt` / `verify/before_pytest.txt` —— 修复后 20 passed / 修复前 4 failed 16 passed 的原始输出
- `verify/fcntl.py`、`verify/hs_connectors.py` —— 本机跑测所需的两个最小桩（**测试脚手架，不是产品代码**）
- `PR-1196.patch` —— 该 PR 的完整 patch
