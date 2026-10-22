# A 类对外动作留痕：FSDP 用例解耦系列请求 review（2026-10-22）

用户授权（本会话）：先 @ 两个人、只发两个 PR。首个方案被否掉的写法已删（不提 CI、不提 NPU/平台、不写具体改动）。
用户明确：改动细节不写；CI 不写；平台不写（"实际我在 GPU 也验证过"）；第一段只保留问号前的句子；第二段再粗一点。

## 实际发出的正文（逐字）

```
/cc @d4l3k @kapilsh — could someone take a look at this one from the FSDP test-decoupling series?

Verified on real hardware.
```

- 署名账号：`li-lizhe`（我们）
- 名单口径：`d4l3k`、`kapilsh` = API 实测近 30 天真发过 `@pytorchbot merge` / approve 的 distributed 维护者
- 第二条（方括号那版「逐 PR 换读数」）已被用户否掉，未发

## 落库记录（API 回读确认）

| PR | 文件 | comment id | 时间(UTC) | URL |
|---|---|---|---|---|
| #192696 | test/distributed/fsdp/test_fsdp_fine_tune.py | 6329361741 | 2026-10-22T00:06:10Z | https://github.com/pytorch/pytorch/pull/192696#issuecomment-6329361741 |
| #192697 | test/distributed/fsdp/test_fsdp_flatten_params.py | 6329362084 | 2026-10-22T00:06:12Z | https://github.com/pytorch/pytorch/pull/192697#issuecomment-6329362084 |

两个 PR 评论区末尾各多一条，发帖人 `li-lizhe`，正文与上表逐字一致（回读核对通过）。

## 未发（等用户点头）

- 余下四条：`#192699`（exec_order）、`#192700`（dtensor_state_dict）、`#192701`（comm）、`#192208`（tp_integration）
- `#192208` 待定项：其 3 条用例需 4 张加速器，我实测那台只有 2 张 ⇒ 全部 skipped。
  若与其余五条同文（"Verified on real hardware."），需用户确认按「文件能在真机跑起来」这一口径接受。

## 复核到的两个事实更正

1. **#192694 是 closed、未合入**（上轮我误记为「已合入」）。六个 PR 所引的
   `requires_world_size` / `HardwareClassification` 在 **main 上已存在**（main 版
   `requires_world_size` 已用 `torch.accelerator.device_count()`，硬件无关），
   「不依赖未合入前置」这一结论不受影响。
2. 六个 PR 的 head SHA 上 **CI run 数 = 0**（base 与 fork 两侧都查了），
   checks 只有 Dr.CI / Meta Internal-Only / capture 三个非构造类 check。
   按用户指示，此事**不写进对外评论**。
