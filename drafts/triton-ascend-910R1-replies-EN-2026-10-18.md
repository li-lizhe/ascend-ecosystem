# triton-ascend #2531 / #2530 / #2529 — English reply drafts (CANN 9.1.0 re-check round)

> **Internal note (do not paste): pending user approval, not yet posted.** 2026-10-18.
> Chinese source of truth: `triton-ascend-910R1-replies-2026-10-16.md` (same folder).
> All numbers taken from raw stdout under `evidence_910/` (D:\ascend\work\issue5376\evidence_910), not from summaries.
> Posting order still to be decided: #2531 / #2530 first, #2529 after self-check (see internal notes at the end of the Chinese file).

---

## Reply for #2531

Thanks for taking a look. First a clarification on the version string, then the CANN 9.1.0 results you asked for.

### 1. `triton-ascend 3.5.0` is not a typo — it is an output value

That number is what `triton.__version__` **prints**, not our distribution version. The pip package in our
environment is `triton-ascend 3.6.0+git0cfb1708` (a local build based on the triton 3.5.0 baseline), so
`import triton; print(triton.__version__)` prints `3.5.0`. What we run is therefore **TA 3.6.0**, which is
consistent with your constraint that TA 3.6.0 is only compatible with CANN 9.1.0. Sorry for the confusion —
we will quote the pip package version from now on.

### 2. Re-run on CANN 9.1.0 as requested: reproduced, and worse than on 9.2.0

Self-contained script `repro_2531.py` — depends only on `torch` + `torch_npu`, **no pytest and no test tree**.
It runs on CANN 9.1.0, and we ran the same script on CANN 9.2.0-beta.2 as a control.

Environment (the two arms differ **only** in CANN):

| Item | Value |
|---|---|
| Device | Ascend910B4 · Python 3.12.13 |
| torch | 2.15.0.dev20260917+cpu |
| torch_npu | 2.15.0.dev20260917+gitec69335 (ec693356f4) |
| triton-ascend | 3.6.0+git0cfb1708 (`triton.__version__` = 3.5.0) |
| backend | `TORCHINDUCTOR_NPU_BACKEND=triton_experimental` |
| Arm A | CANN 9.1.0 (inner version `V100R001C25B114`) |
| Arm B | CANN 9.2.0-beta.2 |

Case: `size=96, nh=4, head_dim=32, seed=0`, fp16 and bf16;
`F.scaled_dot_product_attention` with an upper-triangular `-inf` attn_mask, eager vs `torch.compile`.
A **fp32 CPU eager** run is used as ground truth, to determine which side is wrong.

| dtype | Arm | bitwise ≠ | over rtol/atol=1e-3 | maxdiff | eager vs fp32 | compiled vs fp32 |
|---|---|---|---|---|---|---|
| fp16 | **9.1.0** | 12156/12288 | 11661/12288 | **0.618896** | 0/12288 | **11674/12288** |
| bf16 | **9.1.0** | 11187/12288 | 11185/12288 | **0.605469** | 1379/12288 | **11193/12288** |
| fp16 | 9.2.0 | 11917/12288 | 9826/12288 | 0.073242 | 0/12288 | 9936/12288 |
| bf16 | 9.2.0 | 10031/12288 | 10027/12288 | 0.074219 | 1379/12288 | 9992/12288 |

### 3. Conclusion

1. **Reproduced on CANN 9.1.0 + TA 3.6.0** as well.
2. The fp32 ground truth shows **the compiled branch is the wrong one** (fp16 eager bad = 0/12288, i.e. eager
   matches fp32) — so this is neither an eager problem nor an fp16/bf16 precision issue.
3. The deviation on 9.1.0 is **about 8× larger** than on 9.2.0-beta.2 (compiled vs fp32 maxdiff 0.619 vs 0.073).

> We note that you verified no issue occurs on mainline and in the CANN 9.1.0 scenario. Our TA is
> `3.6.0+git0cfb1708` (built 2026-08-06), which may differ from your current mainline. Running the attached
> script once on your mainline + CANN 9.1.0 should immediately show where the two diverge.

**Raw logs**: `q2_910_cann9100.log` / `q2_910_cann920b2.log`

---

## Reply for #2530

First, the version question: `triton-ascend 3.5.0` is the **output of `triton.__version__`**, not our
distribution version. The pip package is `triton-ascend 3.6.0+git0cfb1708` (a local build based on the triton
3.5.0 baseline) — so what we run is TA 3.6.0.

### Re-run on CANN 9.1.0 as requested: reproduced

Self-contained script `repro_2530.py` (only `torch` + `torch_npu`; it pins `R0_BLOCK` via
`torch_npu._inductor.triton_experimental.config.pin_xr` and runs each configuration in its own process,
so it needs **no pytest and no modification of the installation tree**).

Case: `x = torch.rand(128, 256)` on npu, `torch.compile(lambda t: t.max(dim=1))`, comparing the compiled
`.indices` against the eager `.indices` (== `x.argmax(1)`).

| R0_BLOCK | r-loop split? | CANN 9.1.0 index wrong | CANN 9.2.0-beta.2 index wrong | value wrong | (compiled-eager) diff |
|---|---|---|---|---|---|
| 256 (= rnumel) | no, 1 chunk | 0/128 | 0/128 | 0/128 | {0} |
| 128 | yes, 2 chunks | **55/128** | **55/128** | 0/128 | {-128, 0} |
| 64 | yes, 4 chunks | **89/128** | **89/128** | 0/128 | {-192,-128,-64,0} |

rnumel sweep (default path, CANN 9.1.0): 32→0, 64→0, 128→64/128, 256→89/128, 512→0.

### Conclusion

1. Reproduced on **CANN 9.1.0**, and **identical, digit for digit, to 9.2.0-beta.2** (both arms produce exactly
   the same numbers).
2. **Any split of the r-loop (`R0_BLOCK < rnumel`) produces wrong indices**; with no split (single chunk) the
   result is correct — so the variable is "whether the r-loop is split", not the CANN version.
3. Symptom: **values are always correct, only the indices are wrong**, and the deviation is always an integer
   multiple of the chunk size (`diff ∈ {-192,-128,-64,0}`) — i.e. the compiled side stores the index local to
   the r-chunk and loses the chunk offset. First example: `true_argmax=129, eager=129, compiled=1, diff=-128`.
4. This is a **silent numerical error** (no exception, no crash), so we would suggest prioritising it.

**Raw logs**: `q3_910_repro_cann9100.log` / `q3_910_repro_cann920b2.log` / `q3_910_pin2.log` / `q3_910_rnumel.log`

> On `pin_xr`: it is your own diagnostic knob, so please tell us whether pinning `R0_BLOCK` with it is
> acceptable. If you would rather have a "natural" trigger (no pinning, split caused by the size itself), our
> rnumel sweep already gives directly reproducible sizes: `rnumel=128 → 64/128`, `256 → 89/128`.

---

## Reply for #2529

**We could not reproduce the segfault on CANN 9.1.0.** Below is the investigation and what we observed.

### 1. Re-running the path described in the issue on CANN 9.1.0: the case is SKIPPED, so it could not be verified

The literal command (from the issue) gives **2 skipped, exit=0 on both arms** (CANN 9.1.0 and 9.2.0-beta.2):

> `SKIPPED ... test_combo_kernels.py:425: requires gpu and triton`

The case carries `@requires_gpu_and_triton`, and NPU does not satisfy its GPU check (a long-standing gap —
NPU is not counted as GPU). ⇒ **the case is skipped wholesale on NPU and could not be verified** (this is
**not** the same as "not reproducible").

(Also: the literal command additionally fails with ImportError in our container because the unbuilt `torch/`
source tree in the cwd shadows site-packages; changing cwd to `/tmp` plus absolute paths collects normally.
Unrelated to this issue, mentioned only for completeness.)

### 2. To actually reach the case we opened that gate with a runtime shim (no install-tree changes)

Using `patch_npu_shim.py` (only `setattr` on already-imported modules, no installed file touched) to bypass
`requires_gpu_and_triton`, both arms give:

| Arm | Result |
|---|---|
| CANN 9.1.0 | `rc=1` FAIL — `NoTritonConfigsError ... CompilationError ... NameError('x0_blocks is not defined')` |
| CANN 9.2.0-beta.2 | `rc=1` FAIL — same error |

**Neither arm segfaults (no 139 / SIGSEGV).** The failure happens at **compile time**: in the generated
`triton_unk_fused_0`, `group_size = x0_blocks // total_thread` references an undefined `x0_blocks`.

### 3. Direct probe (explicit combo kernels + consecutive compiles)

`probe_2529.py`: explicitly enables combo kernels, compiles 4 graphs consecutively in one process plus 3
repeated compiles, and both arms × `per_subkernel_blocks ∈ {0,1}` all end with
`ALL_DONE_NO_SEGFAULT` (exit 0); failures are all **compile-time** `NameError` (`x0_blocks` / `x0`
undefined), not a crash.

### 4. Conclusion and request

- On **CANN 9.1.0** we **did not observe a segfault**: the literal case is skipped (not verified); both the
  forced-gate path and the direct probe end in a **compile-time NameError**, not 139.
- The segfault in our original report may come from **a different trigger path** (or from the specific
  combination of combo-kernel switch / `per_subkernel_blocks` we used at the time). We **cannot reproduce it
  stably at the moment**, so we will not claim anything about its state on 9.1.0.
- 🙋 **Could you point us to the path?** How should that segfault be triggered on your side (e.g. a specific
  test id, switch combination, or number of consecutive compiles)? Re-running 9.1.0 along the path you give
  will be far more efficient than us guessing.
- Separately: the `NameError('x0_blocks is not defined')` above (a combo kernel failing to emit the
  `x0_blocks` definition) looks like **another** real defect (it hits both 9.1.0 and 9.2.0). If it is in fact
  the same root cause as this issue, please tell us and we will fold it into this thread instead.

**Raw logs**: `q4_910_cann9100.log` / `q4_910_cann920b2.log` (literal SKIP),
`q4_910_gate_cann9100.log` / `q4_910_gate_cann920b2.log` (forced gate),
`q4_910_probe_*_ps*.log` (direct probe)
