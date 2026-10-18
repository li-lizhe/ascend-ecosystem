# issue2530 —— #2530 修复实证（已提 PR #2615）

**日期**：2026-10-18　**PR**：triton-lang/triton-ascend **#2615**
**议题**：triton-ascend #2530 归约轴被 split 时 index 归约丢 chunk 偏移

---

## 0. 一句话

**补丁有效性已真机确证：三组读数全归零。**

| `R0_BLOCK` | 打补丁前 | 打补丁后 |
|---|---|---|
| 256（不切分） | 0/128 | 0/128 |
| 128 | **错 55/128** | **0/128** ✅ |
| 64 | **错 89/128** | **0/128** ✅ |

---

## 1. 根因

消费端 AscendNPU-IR `LinalgToHFusion.cpp` 只在该 operand 带 `UseIndexInput` 注解时
才把 index 透传给 `hfusion.reduce_with_index`；而 **triton-ascend 全仓 0 处产出该注解**
⇒ 开关装好没人合闸 ⇒ index 被丢、下游模板自造 `0..chunk-1` 局部下标。
值仍正确，但归约轴一被 split（`R0_BLOCK < rnumel`），返回的 index 就是 chunk 局部而非全局。

**补丁**：在 `reduce_mode` 已设置处（`ReduceConverter::convertToTargetOpExtended`，
`TritonOpConverter.cpp`）给 index operand 补上 `annotation::MarkOp` + `UseIndexInput`
（+20 行，含 InsertionGuard 与幂等检查）。

---

## 2. 环境与产物

| 项 | 值 |
|---|---|
| 机器 | 169 容器 `npu-l00534385` |
| 芯片 / CANN | Ascend 910B2 / 9.2.0-beta.2 |
| 源码 ref | `0cfb1708`（= 实装包 `triton_ascend-3.6.0+git0cfb1708`） |
| LLVM | `f6ded0be`（宿主已有 4.6G 现成件） |
| AscendNPU-IR | `d4405acb` |
| 产物 | `libtriton.so` **172.5 MB**、**0 编译错误**、848 目标 |
| md5（双向核对一致） | `2ce148864d9d17e82188276e1688f9f4` |

**★ 必须与实装包同 ref 编译**：用 `main`（LLVM22）会死在
`error: attempting to parse a byte at the end of the bytecode ... MLIR22.0.0git`
—— CANN 9.2.0 的 bishengir 解析不了 LLVM22 字节码，与补丁无关。

---

## 3. 验证方法（单变量）

**同一份 `verify_fix.py`、同一环境，只替换 `libtriton.so` 一个文件**，
`md5sum` 核对装进去的确实是自编那份 ⇒ 读数差异只能归因于补丁。

---

## 4. lit 测试真跑通过

新增 `third_party/ascend/unittest/Conversion/General/TritonToLinalg/use_index_input_annotation.mlir`
（66 行 / 3 用例：max_with_index、min_with_index、普通归约断言 `CHECK-NOT: annotation.mark`）。

```
$ triton-opt --triton-to-linalg="named-ops=True" --split-input-file <测试> | FileCheck <测试>
FILECHECK_PASS
```

---

## 5. PR #2615 内容

| 文件 | 变化 |
|---|---|
| `third_party/ascend/lib/TritonToLinalg/TritonOpConverter.cpp` | +20 |
| `third_party/ascend/unittest/Conversion/General/TritonToLinalg/use_index_input_annotation.mlir` | +66（新增） |

正规表达式 `Fixes #2530`；已按官方 PR 模板写正文（含新贡献者 checklist）。
仓库 open PR 计数：本 PR 前 2（#2454 / #2449），本 PR 后 **3**。

---

## 6. 证据等级

| 项 | 等级 |
|---|---|
| 编译成功（172.5MB / 0 错误） | **实测** |
| 补丁前后读数（55/128、89/128 → 0/128） | **实测**（单变量：只换 `libtriton.so`） |
| lit 测试 `FILECHECK_PASS` | **实测** |
| PR 已创建、字段与改动文件数 | **实测**（API 回读） |
| PR CI 结果 | **未取**（刚开） |
