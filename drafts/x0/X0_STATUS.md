# X0 线状态（2026-10-19）

## 1. 结论先说：两条 issue 都**早已存在**，且都归我们名下

GitCode `Ascend/pytorch` 实查（token 走 `gc-token`）：

| issue | 标题 | 状态 | 负责人 | 我们已发评论 |
|---|---|---|---|---|
| **#5281** | 【硬件解耦任务】【torch-npu】combo kernel 生成代码引用未定义变量 x0，import 时 NameError | open | 无 assignee | **10-13 已发根因帖（1742 字）** |
| **#5374** | 【硬件解耦任务】[Bug]: 组合核路径上间接索引（`index`）未保留在 triton 内，gather 无法融进组合核 | open | **lizhe_li** | 10-13 已回「正常提PR，性能问题在PR中讨论」 |
| #5375 | 组合核发出的 `inductor_meta` 键集与单独内核不一致 | open | lizhe_li | 3 条 |
| #5376 | `aten.cumsum` 未保留上游实现 ⇒ 组合核里没有 `_triton_helper_fn` | open | lizhe_li | 4 条 |

⇒ 用户交代的「X0 线」（生成代码引用未定义 x0）**不需要新开 issue**，
它就是 **#5281**，且根因帖我们在 10-13 已经发过。

## 2. #5281 根因（我们 10-13 发的原文要点）

比「缺 x0 定义」更靠前一层：

1. NPU 后端把整个 x-tree header（`x0offset`/`x0index`/`x0 = x0index`/`x0mask`/`xmask`）
   **全部**发射在 `codegen_range_tree()`（`npu_header.py:1101/1103/1118`）；
2. **combo 子内核从未被 linearize**：`_apply_linearize` 在 `len(kernels) > 1` 时
   被传 `None`（`codegen/triton.py:5541`），函数开头 `if kernel is None: return` 直接跳过
   ⇒ 子内核 `tree.nodes` 为空；
3. 即便 `_apply_linearize` 内部（`codegen/triton.py:7311`）会**重调** `codegen_range_tree()`…

复现：上游 `test/inductor/test_combo_kernels.py` 的
`test_noinline_sub_kernel_body_dedupes_by_signature`，不前置任何运行期补丁即 100%
编译期复现（约 20s）。

## 3. 实装树现状（169 容器）

`torch_npu/_inductor/triton_experimental/codegen/triton.py`：

- `_apply_linearize` 调用点仍在 **5598 行**：
  `self._apply_linearize(kernels[0] if len(kernels) == 1 else None, node_schedule)`
  ⇒ **实装版仍是「combo 时传 None」的老逻辑**；
- 函数定义在 6746 行；
- 全文件有 3 处 `npu_header|linearize_combo` 相关标记（非我们补丁名）。

## 4. 待做

1. 复核 `history/round20_r13_evidence/fix_defect7.patch`（241 行，只改
   `triton_experimental/codegen/triton.py`）：
   - 是否就是 #5281 的修法；
   - 在实装版上 `git apply --check`；
   - 真机跑上游用例验证（先拿 RED 基线）。
2. 另两条（#5374 index、#5375 inductor_meta 键集）的补丁同批复核。
   ⚠️ 待提交稿 13（index 那条）**自带诚实负面结论：master 上 0 F→P**，
   ⇒ **不可照原样提交**，需先重测。
3. 结论齐了再排 PR（本仓 open MR = 0，额度不紧张）。
