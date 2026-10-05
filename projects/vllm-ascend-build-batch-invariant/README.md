# vllm-ascend #17784 — build_batch_invariant_ops.sh exits 0 on failure

- Issue: https://github.com/vllm-project/vllm-ascend/issues/17784
- PR:    https://github.com/vllm-project/vllm-ascend/pull/17888  (+18/-1, 1 file)
- Base commit: `7df9604`
- Change: `csrc/build_batch_invariant_ops.sh` now tracks any download/install
  failure in a `FAILED` flag and `exit "${FAILED}"` at the end, instead of
  always reaching the last line and exiting 0.

## Why it is a real bug

Every failing command in the script is wrapped in an `if`/`||` context, so
`set -euo pipefail` never fires and the failure is silently swallowed. The
caller chain `csrc/build_aclnn.sh` (bare call under `set -e`) -> `setup.py`
(`subprocess.check_call([... "csrc/build_aclnn.sh", ...])`, line 199) therefore
treats the build as successful even when the batch-invariant ops were never
installed (numerical-behaviour difference, not just a missing optimisation).

## Verification (no NPU needed — stubbed download/installer)

`verify/` drives each branch by stubbing `curl` (via `PATH`) and the installer.
Run `bash verify/run_all.sh` (output in `verify/output.txt`).

| Scenario                | Before | After |
|-------------------------|--------|-------|
| both downloads fail     | exit 0 | exit 1 |
| run-package installer fails | exit 0 | exit 1 |
| everything succeeds     | exit 0 | exit 0 (unchanged) |

Not tested: a real end-to-end `pip install .` on Ascend hardware / CANN.
