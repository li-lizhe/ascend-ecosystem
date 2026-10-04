# apache/brpc — fuzzing harnesses return an illegal value from `LLVMFuzzerTestOneInput`

- **PR**: https://github.com/apache/brpc/pull/3579 (open, 18 files, +18/−18, 1 commit)
- **Issue**: https://github.com/apache/brpc/issues/3578
- **Round**: 2026-10-04 晚 21 点探新流水线（178 仓池 · T1）
- **验证等级**: 🟡（本机无 brpc 构建环境；用 clang 17 / openEuler 24.03 / aarch64 驱动 + 真 libFuzzer 实跑验证契约）

## 问题

`test/fuzzing/` 下 18 个 harness 都以同一个尺寸闸门开头：

```c
if (size < kMinInputLength || size > kMaxInputLength){
    return 1;          // 不是合法的返回码
}
```

libFuzzer 只接受 `0`（已消费）或 `-1`（拒绝该输入），并在每次调用后断言
`assert(CBRes == 0 || CBRes == -1)`（`compiler-rt/lib/fuzzer/FuzzerLoop.cpp:622`）。
libFuzzer 的第一个输入是空输入（size=0 < kMinInputLength），所以**开 assert 的 libFuzzer
在启动阶段就会 abort 全部 18 个 harness**。release 版 libFuzzer 跳过断言、把 `1` 当 `-1`，
所以 CI/OSS-Fuzz 一直没暴露。

## 修法

18 个文件里 `return 1;` → `return 0;`（仅尺寸闸门那一行，共 18 行）。
选 `return 0` 而不是 `-1`：两者都满足契约，`0` 与较新 harness（#3516 的
`test/fuzzing/fuzz_rtmp.cpp`）的写法一致；越界输入仍然不会进入 harness 主体，
在范围内的输入行为完全不变。

## 验证（🟡，clang 17.0.6 + openEuler 24.03 + aarch64）

驱动复刻 libFuzzer 的返回码契约（原文 `assert(CBRes == 0 || CBRes == -1)`），
首个输入取空输入：

| 构建 | `LLVMFuzzerTestOneInput(empty, 0)` | 结果 |
| --- | --- | --- |
| 修复前（`return 1`） | `1` | `Assertion 'r == 0 || r == -1' failed` → `Aborted (core dumped)`，exit 134 |
| 修复后（`return 0`） | `0` | `return-value contract satisfied: CBRes=0`，exit 0 |

修复后的 harness 用真 libFuzzer 链接运行：`clang++ -std=c++17 -fsanitize=fuzzer`，
`./fuzz -runs=5` → `Done 5 runs in 0 second(s)`，exit 0。

**未测**：完整 brpc 构建 + OSS-Fuzz 实际跑（harness 要链接 brpc 各库，本机未构建）；
改动只是每个文件一个返回值，不触碰任何 harness 逻辑。

## 证据文件

- `verify_return_contract.cpp` — 契约驱动源码（含 `-DBEFORE_FIX` 开关复现原缺陷）
- `verification-fuzz-return-code.txt` — 上文两次编译/运行的原始输出
