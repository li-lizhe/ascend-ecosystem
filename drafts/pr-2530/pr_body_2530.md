### What

Annotate the index operand of a `max_with_index` / `min_with_index` reduction with `UseIndexInput`, so `LinalgToHFusion` keeps forwarding it to `hfusion.reduce_with_index`.

### Why

`LinalgToHFusion.cpp` only keeps the index input when that operand carries the `UseIndexInput` annotation:

```cpp
std::optional<Operation *> isIndexInputUnused =
    utils::getAnnotateOpWithAttr(op.getInputs()[1], "UseIndexInput");
if (isIndexInputUnused.has_value()) {
  inputs = op.getInputs();              // keep the index tensor
} else {
  inputs.push_back(op.getInputs()[0]);  // index dropped
}
```

Nothing in the pipeline produced `UseIndexInput` (`grep -rn UseIndexInput` is empty on the triton-ascend side), so the `else` branch always ran: the index tensor was dropped and the downstream `reduce_*_with_index` template synthesised `0..chunk-1` local indices. The values stayed correct, but the returned indices are chunk-local instead of global as soon as the reduction axis is split (`R0_BLOCK < rnumel`).

The fix sets the annotation where `reduce_mode` is already set, in `ReduceConverter::convertToTargetOpExtended`, so the templated `..._with_specified_index` variant is selected and looks the global index up instead of regenerating a local one.

### Reproduction and measurement

Ascend 910B2, CANN 9.2.0-beta.2, `test_reduce_functions`-style case reduced to `x.max(dim=1)` on a `128x256` fp32 tensor, with the reduction axis split at `R0_BLOCK`:

| `R0_BLOCK` | before | after |
|---|---|---|
| 256 (no split) | 0/128 wrong | 0/128 wrong |
| 128 | **55/128 wrong** | **0/128 wrong** |
| 64 | **89/128 wrong** | **0/128 wrong** |

The "after" column was produced by rebuilding `triton-ascend` with this patch, replacing only `libtriton.so`, and rerunning the same script and the same `R0_BLOCK` values.

### Tests

Added `third_party/ascend/unittest/Conversion/General/TritonToLinalg/use_index_input_annotation.mlir`, which checks that `max_with_index` / `min_with_index` produce `annotation.mark ... {UseIndexInput}`, and that a plain reduction does not.

```
$ triton-opt --triton-to-linalg="named-ops=True" --split-input-file use_index_input_annotation.mlir | FileCheck use_index_input_annotation.mlir
FILECHECK_PASS
```

Verified output:

```mlir
annotation.mark %arg1 {UseIndexInput} : tensor<2x4xi32>
%reduced:2 = linalg.reduce ins(%arg0, %arg1 : tensor<2x4xf32>, tensor<2x4xi32>) outs(%0, %1 : tensor<2xf32>, tensor<2xi32>) dimensions = [1]  {reduce_mode = "max_with_index", ...}
```

### New contributor declaration

- [x] I am not making a trivial change, such as fixing a typo in a comment.
- [x] I have written a PR description following these [rules](https://cbea.ms/git-commit/#why-not-how).
- [ ] I have run `pre-commit run --from-ref origin/main --to-ref HEAD`.
- Select one of the following.
  - [x] I have added tests.
    - `/test` for `lit` tests
- Select one of the following.
  - [x] I have not added any `lit` tests.
  - [x] The `lit` tests I have added follow these [best practices](https://mlir.llvm.org/getting_started/TestingGuide/#filecheck-best-practices), including the "tests should be minimal" section.

Fixes #2530
