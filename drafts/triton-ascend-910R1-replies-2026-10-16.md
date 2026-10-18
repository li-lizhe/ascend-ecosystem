# triton-ascend #2529 / #2530 / #2531 回帖草稿（CANN 9.1.0 复核轮 910-R1）

> **状态：草稿，未经用户确认不得发布。** 2026-10-16 起草。
> 口径依据：维护者 Skyminers 在 #2530/#2531 要求「提供 CANN 9.1.0 上能复现的测试用例」。
> 全部数字来自实测原始 stdout（evidence_910/），未作任何全称结论。

---

## 一、草稿 #2531（静态 r-numel 特化 ⇒ fused softmax 行 max 归约误编译 / SDPA+mask 数值错）

感谢复核。先澄清版本号，再给 CANN 9.1.0 的实测结果。

### 1. `triton-ascend 3.5.0` 不是笔误

那是 `triton.__version__` 的**输出值**，不是发行版号。我们环境里 pip 包版本是
`triton-ascend 3.6.0+git0cfb1708`（基于 triton 3.5.0 基线的本地构建），所以
`import triton; print(triton.__version__)` 打印 `3.5.0`。我们跑的确实是 **TA 3.6.0**，
与你们「3.6.0 只兼容 CANN 9.1.0」的约束是对得上的。这个写法造成了误会，抱歉，
我们后续一律写 pip 包版本。

### 2. 按你们要求的 CANN 9.1.0 复跑：复现，且比 9.2.0 更严重

我们写了**自包含**脚本 `repro_2531.py`（只依赖 torch + torch_npu，**不依赖 pytest 或任何测试树**），
在 CANN 9.1.0 上跑通，并在 CANN 9.2.0-beta.2 上跑同一条做对照。

环境（两臂**只换 CANN**，其余完全相同）：

| 项 | 值 |
|---|---|
| 设备 | Ascend910B4 · Python 3.12.13 |
| torch | 2.15.0.dev20260917+cpu |
| torch_npu | 2.15.0.dev20260917+gitec69335 (ec693356f4) |
| triton-ascend | 3.6.0+git0cfb1708（`triton.__version__`=3.5.0） |
| backend | `TORCHINDUCTOR_NPU_BACKEND=triton_experimental` |
| 臂 A | CANN 9.1.0（innerversion `V100R001C25B114`） |
| 臂 B | CANN 9.2.0-beta.2 |

用例：`size=96, nh=4, head_dim=32, seed=0`，fp16 与 bf16；
`F.scaled_dot_product_attention` + 上三角 `-inf` attn_mask，eager vs `torch.compile`。
额外用 **fp32 CPU eager 作为真值**，用于判定到底哪一侧错。

| dtype | 臂 | bitwise≠ | 超 rtol/atol=1e-3 | maxdiff | eager vs fp32 | compiled vs fp32 |
|---|---|---|---|---|---|---|
| fp16 | **9.1.0** | 12156/12288 | 11661/12288 | **0.618896** | 0/12288 | **11674/12288** |
| bf16 | **9.1.0** | 11187/12288 | 11185/12288 | **0.605469** | 1379/12288 | **11193/12288** |
| fp16 | 9.2.0 | 11917/12288 | 9826/12288 | 0.073242 | 0/12288 | 9936/12288 |
| bf16 | 9.2.0 | 10031/12288 | 10027/12288 | 0.074219 | 1379/12288 | 9992/12288 |

### 3. 结论

1. 在 **CANN 9.1.0 + TA 3.6.0** 上**同样复现**；
2. fp32 真值显示：**错的是 compiled 分支**（fp16 eager bad = 0/12288），
   eager 与 fp32 一致 ⇒ 不是 eager 的问题，也不是 fp16/bf16 精度。
3. 9.1.0 的偏差**比 9.2.0-beta.2 大约 8 倍**（compiled vs fp32 maxdiff 0.619 vs 0.073）。

> 我们注意到你们已确认「mainline 与 CANN 9.1.0 场景下未出现该问题」。
> 我们的 TA 是 `3.6.0+git0cfb1708`（2026-08-06 构建），可能与你们当前 mainline 有差异。
> 用我们附的脚本在你们 mainline + CANN 9.1.0 上跑一次，应该能立刻看出差异在哪。

**原始日志**：`q2_910_cann9100.log` / `q2_910_cann920b2.log`

### 待确认点
1. 是否需要把「`triton.__version__`=3.5.0 是输出值、pip 包实为 3.6.0」这段澄清写进回帖，
   还是只改我们 issue 正文？
2. `repro_2531.py` 用**附件**还是贴进正文？（约 7 KB）
3. 是否同时报 9.2.0 对照？——利弊：能证明「单一变量对照」，但可能被追问「9.2.0 是否也算问题」。
4. 是否要附上 fp32 真值那段（最有说服力，但会让回帖变长）。

---

## 二、草稿 #2530（归约轴被 split（R0_BLOCK < rnumel）时 index 归约丢 chunk 偏移）

先回答版本号：`triton-ascend 3.5.0` 是 `triton.__version__` 的**输出**，不是发行版号。pip 包实为
`triton-ascend 3.6.0+git0cfb1708`（基于 triton 3.5.0 基线本地构建），即我们跑的就是 TA 3.6.0。

### 按你们要求的 CANN 9.1.0 复跑：复现

自包含脚本 `repro_2530.py`（只依赖 torch + torch_npu；用 `torch_npu._inductor.triton_experimental.config.pin_xr`
固定 `R0_BLOCK`，每个配置独立进程，因此**不需要 pytest、不需要改安装树**）。

用例：`x = torch.rand(128, 256)` on npu，`torch.compile(lambda t: t.max(dim=1))`，
比较 compiled `.indices` 与 eager `.indices`（== `x.argmax(1)`）。

| R0_BLOCK | r-loop 是否切分 | CANN 9.1.0 index 错 | CANN 9.2.0-beta.2 index 错 | value 错 | (compiled-eager) diff |
|---|---|---|---|---|---|
| 256 (=rnumel) | 否，1 chunk | 0/128 | 0/128 | 0/128 | {0} |
| 128 | 是，2 chunks | **55/128** | **55/128** | 0/128 | {-128, 0} |
| 64 | 是，4 chunks | **89/128** | **89/128** | 0/128 | {-192,-128,-64,0} |

rnumel 扫描（默认路径，CANN 9.1.0）：32→0、64→0、128→64/128、256→89/128、512→0。

### 结论

1. 在 **CANN 9.1.0** 上复现，且与 9.2.0-beta.2 **逐字一致**（两臂数值完全相同）。
2. **只要 r-loop 被切分（`R0_BLOCK < rnumel`）就会错**；不切分（单 chunk）时正确 ⇒ 变量是「是否切分」，
   不是 CANN 版本。
3. 表现：**value 全对、只有 index 错**，且偏差恒为 chunk 大小的整数倍
   （`diff ∈ {-192,-128,-64,0}`）⇒ compiled 侧存的是 r-chunk **内部**的局部下标，丢了 chunk 偏移。
   首例：`true_argmax=129, eager=129, compiled=1, diff=-128`。
4. 这是**静默数值错**（不报错、不崩溃），建议优先。

**原始日志**：`q3_910_repro_cann9100.log` / `q3_910_repro_cann920b2.log` / `q3_910_pin2.log` / `q3_910_rnumel.log`

### 待确认点
5. `pin_xr` 是你们自带的诊断旋钮，用它固定 `R0_BLOCK` 是否可接受？若你们希望用更「真实」的触发方式
   （不 pin、靠尺寸自然切分），我方 rnumel 扫描已给出 `rnumel=128 → 64/128`、`256 → 89/128` 的可直接复现尺寸。

---

## 三、草稿 #2529（launcher 把 KernelMetadata 当 dict ⇒ 同进程连续编译组合核 segfault）

这条**我们无法用 9.1.0 复现 segfault**，如实说明排查过程和目前的观察。

### 1. 按 issue 里的路径在 CANN 9.1.0 上复跑：用例被 SKIP，未能验证

字面命令（`cd /opt/npu-env/pytorch_src_215` + `pytest -k test_reduce_functions`）在
CANN 9.1.0 与 9.2.0-beta.2 上**两臂均 2 skipped, exit=0**：

> `SKIPPED ... test_combo_kernels.py:425: requires gpu and triton`

原因是该用例带 `@requires_gpu_and_triton`，而 NPU 不满足其 GPU 判定（历史坑，NPU 不被算作 GPU）。
⇒ **本用例在 NPU 上被整体跳过，未能验证**（这**不等于**「不复现」）。

（另：字面命令在本容器还会因 cwd 下未编译的 `torch/` 源码树遮蔽 site-packages 而 ImportError；
把 cwd 换成 `/tmp` + 绝对路径即可正常收集。这点与本 issue 无关，一并说明。）

### 2. 为真正触达该用例，我们用运行期 shim 打开了这个门（不改安装树）

用 `patch_npu_shim.py`（只 setattr 已导入的模块、不动任何安装文件）绕过 `requires_gpu_and_triton`
后，两臂得到：

| 臂 | 结果 |
|---|---|
| CANN 9.1.0 | `rc=1` FAIL — `NoTritonConfigsError ... CompilationError ... NameError('x0_blocks is not defined')` |
| CANN 9.2.0-beta.2 | `rc=1` FAIL — 同一错误 |

**两臂都没有 segfault（无 139 / SIGSEGV）。** 失败发生在**编译期**：
生成的 `triton_unk_fused_0` 里 `group_size = x0_blocks // total_thread` 引用了未定义的 `x0_blocks`。

### 3. 直接探针（显式开组合核 + 连续编译）

`probe_2529.py`：显式打开组合核、同进程连续编译 4 个图 + 3 次重复编译，
两臂 × `per_subkernel_blocks∈{0,1}` 全部 `ALL_DONE_NO_SEGFAULT`（exit 0）；
失败者均为**编译期** `NameError`（`x0_blocks` / `x0` 未定义），非崩溃。

### 4. 结论与请求

- 在 **CANN 9.1.0** 上**未观察到 segfault**：字面用例被 skip（未能验证）；强开门与直接探针两条路径
  都是**编译期 NameError**，不是 139。
- 我们原始报告中的 segfault 可能来自**另一条触发路径**（或与我们当时的组合核开关/per_subkernel_blocks
  组合有关），目前我们**无法稳定复现**，因此不敢断言它在 9.1.0 上的状态。
- 🙋 **请指教**：该 segfault 的路径在你们那边应如何触发（例如某个具体 test id / 开关组合 /
  连续编译次数）？我们按你们给的路径再跑 9.1.0，比我们盲猜更有效率。
- 另：上面的 `NameError('x0_blocks is not defined')`（组合核未发射 `x0_blocks` 定义）看起来是**另一个**
  真实缺陷（9.1.0 与 9.2.0 两臂都中）。如果它其实与本 issue 同源，请告知，我们合并到这条跟进。

**原始日志**：`q4_910_cann9100.log` / `q4_910_cann920b2.log`（字面 SKIP）、
`q4_910_gate_cann9100.log` / `q4_910_gate_cann920b2.log`（强开门）、`q4_910_probe_*_ps*.log`（直接探针）

### 待确认点
6. 这条我建议**放软**：不写「不复现」，写「未能验证 + 请指教触发路径」。#2529 原报告里的 segfault
   我们**这次没能重现**——是否需要先自查我们当初那条路径，再回帖？
7. `NameError('x0_blocks is not defined')` 要不要单独立一条新 issue？（两臂都中，是本轮新发现）
8. 是否把我们 issue 正文里「triton-ascend 3.5.0」的写法统一改成 pip 包版本口径（三条一起改）？

---

## 四、发布方式（待确认）
9. 三条分开发（各回各的 issue），一次发完还是先发 #2530/#2531、#2529 等自查后再发？
10. 脚本给附件还是贴正文？仓库里 `evidence_910/` 是否要同步归档进 mindlog history/？
