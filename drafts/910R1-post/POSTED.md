# 910-R1 回帖发布记录（triton-lang/triton-ascend）

> 2026-10-18 发布（中文版，用户 10-18 拍板「中文发吧」）。

| issue | 评论 id | 时间 | 正文来源 | 逐字回读校验 |
|---|---|---|---|---|
| [#2529](https://github.com/triton-lang/triton-ascend/issues/2529#issuecomment-6244147601) | 6244147601 | 2026-10-18T01:2xZ | body_2529.md（5262 chars） | 一致 |
| [#2530](https://github.com/triton-lang/triton-ascend/issues/2530#issuecomment-6244147763) | 6244147763 | 2026-10-18T01:2xZ | body_2530.md（6585 chars） | 一致 |
| [#2531](https://github.com/triton-lang/triton-ascend/issues/2531#issuecomment-6244147939) | 6244147939 | 2026-10-18T01:2xZ | body_2531.md（9891 chars） | 一致 |

发布工具：`post_910R1.py`（`--go` 真发 + 回读校验；`--verify` 只校验）。
正文由 `build_bodies.py` 从 `tpl_<n>.md` + `evidence_910/{repro_2531,repro_2530,probe_2529}.py` 组装，
脚本以 `<details>` 内联在正文中（不挂附件）。

## 已采纳的口径

1. **版本号**：写明 `3.5.0` 是 `triton.__version__` 输出值、pip 包实为 `3.6.0+git0cfb1708`；
   证据是上游 commit `0cfb1708` 的 `version.txt`=3.6.0 而 `python/triton/__init__.py` 里
   `__version__ = '3.5.0'` —— 是上游自身的两处不一致，不是我们的笔误。
2. **#2531/#2530 硬口径**：CANN 9.1.0 复现（#2530 两臂逐字一致）；#2531 附 fp32 真值证明
   错在 compiled 分支，且 9.1.0 偏差约为 9.2.0-beta.2 的 8 倍。
3. **#2529 软口径**：不写「不复现」，写「用例被 SKIP 未能验证 + 强开门/探针都是编译期 NameError（无 139）
   + 🙋 请指教你们的触发路径」；`x0_blocks` 的 NameError 在线程内问是否同源，未另开 issue。
4. 全部数字取自原始 stdout，发布前逐个回原始日志定位核对（脚本见 session）。

## 待跟进

- 等 Skyminers 就 #2529 给出触发路径；若确认 `x0_blocks` 与 #2529 无关，再单独立 issue。
- evidence_910/ 是否归档进 mindlog `history/` 仍待用户指定位置。
