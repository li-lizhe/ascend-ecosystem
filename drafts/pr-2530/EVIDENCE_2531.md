# #2531 取证记录（2026-10-19）

议题：triton-lang/triton-ascend **#2531** —— 静态 r-numel 被烧成编译期常量后，
fp16 SDPA + attn_mask 的行 max / softmax 归约算错。

机器：169 容器 `npu-l00534385`，Ascend910B4，CANN 9.2.0-beta.2，
torch 2.15.0.dev20260917+cpu，torch_npu 2.15.0.dev20260917+gitec69335，triton 3.5.0。

---

## 1. 已确证

### 1.1 基线可复现
`repro_2531.py` 在实装栈上稳定复现：

| dtype | 错行数 |
|---|---|
| fp16 | 9824 / 12288 |
| bf16 | 10027 / 12288 |

### 1.2 单变量 A/B —— 该常量注入是直接成因

改动点（唯一）：`torch_npu/_inductor/triton_experimental/codegen/triton.py:4426`

```python
triton_meta["constants"][numel_name] = int(tree.numel)
```

| 臂 | 该行 | 结果 |
|---|---|---|
| A（现状） | 保留（r0_numel 进 constants ⇒ 编译期常量） | **错 9824 / 12288** |
| B（对照） | 去掉（r0_numel 退回运行时 i32） | **错 0 / 12288** |

同环境、同脚本、只改这一行 ⇒ 该常量注入与错误**因果相关**。

### 1.3 IR 级证据

`TRITON_KERNEL_DUMP=1` 各 dump 50 个文件：

| 阶段 | A 行数 | B 行数 | 差异行数 |
|---|---|---|---|
| ttir | 169 | 190 | 333 |
| ttadapter | 144 | 183 | 317 |
| bcmlir | 145 | 184 | 317 |
| npubin | 34 | 13 | 0（md5 不同） |

两臂在 ttir 即分叉；`mlirbc` md5 不同（A=`a0874547…`，B=`3c33092f…`）。

### 1.4 已知缺口（必须一起说）
两臂**同时**还有第二个差异：real_block_x0（XBLOCK）A=96、B=16，group 数 A=4、B=24。
即「常量注入」与「自动调优选中的 XBLOCK」在该 A/B 里是**联动变化**的，
所以严格说这组对照不满足单变量；因果链的强度是「该行改动导致结果变化」，
而不是「该行是唯一原因」。

---

## 2. 未成立（诚实记录）

试图把缺陷缩成自包含最小内核（不依赖 torch_npu），试了 5 版，全部失败：

| 版本 | 结构 | 结果 |
|---|---|---|
| minimal_2531.py | 2x2 常量/运行时 × XBLOCK 16/96 | 只有「常量+16」格错 80/96 —— **是我自己的 bug**（没取 program_id，各 program 都写同一批行） |
| minimal_2531b.py | 显式 program_id | 6 臂全 ok ⇒ 证明上一版错在 harness |
| k2531_verbatim2.py | 逐字抄真实内核（含 tl.broadcast_to） | 编译不过：`'NoneType' object has no attribute 'type'` |
| k2531_final.py | 结构孪生（3-D tile + group 分发 + 三遍 r 循环） | 4 臂全 ok 0/9216 |
| k2531_flat.py / k2531_max2b.py | 摊平 + `triton_helpers.max2` | max2 可用；`libdevice.exp` 在 3-D 上不可用；4 臂全 ok |

**结论：单独把 r0_numel 变成编译期常量，不构成自包含触发条件。**
真实缺陷还需要第二个因素，尚**未分离出来**。

---

## 3. 下一步（按优先级）

1. **消混淆**：把 A 臂的 XBLOCK 钉成与 B 臂一致（16）再跑。
   - 仍错 ⇒ 常量注入单独成立，1.2 升级为严格单变量；
   - 变对 ⇒ 真正触发在「XBLOCK=96 那组配置」侧，需转去 triton-ascend 的
     reduce 拆分/合并 pass 找落点。
2. 若定位到配置侧，再进 triton-ascend 侧取证（`169` 已具备编译条件，
   见 `triton-ascend-patch-verified-build-recipe`）。
3. 拿到严格结论后再写 issue 评论 / 起草修复 —— **当前证据不足以对外定因**。
