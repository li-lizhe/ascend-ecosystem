# spikingjelly — DSpike search network device-agnostic fix

## Target
- **Repo**: [fangwei123456/spikingjelly](https://github.com/fangwei123456/spikingjelly) (2116★, 100% merge rate, very active)
- **Issue**: No existing issue filed — proactively discovered `.cuda()` hardcoding and surrogate regression
- **PR**: [#748](https://github.com/fangwei123456/spikingjelly/pull/748)

## Problem
`SearchSpikingConv2d_stem`/`SearchSpikingConv2d_cell` in `spike_dhs.py` create the `dgs_alpha` parameter with `torch.ones(3).cuda()`, hardcoding CUDA. Crashes on any non-CUDA backend (Ascend NPU, MPS, CPU-only) with `AssertionError: Torch not compiled with CUDA enabled`.

Additionally, `DSpike.__init__` calls `super().__init__(alpha, spiking)` positionally, but `SurrogateFunctionBase` (refactored in PR #743) now has `__init__(self, spiking=True, **kwargs)`, making the module uninstantiable even on CPU.

## Root Cause
- `.cuda()` hardcodes CUDA-only device assignment in 4 locations.
- Surrogate API regression: DSpike passes `alpha` positionally to a base class that no longer accepts it positionally.

## Fix
1. **Device-agnostic parameter creation**: `.cuda()` → `device=self.conv_m.weight.device` (or `self.conv1_m.weight.device` for cell class). Parameter follows the module's device.
2. **Surrogate call fix**: `super().__init__(alpha, spiking)` → `super().__init__(spiking=spiking, alpha=alpha)`.

## Verification
- `torch.cuda.is_available() == False` on NPU → original `.cuda()` raises AssertionError
- After fix: stem/cell instantiate on NPU with `dgs_alpha.device == npu:0`
- `forward()` correct shape `[2, 16, 32, 32]`
- `dgs_init_stage()` keeps param on NPU
- CPU-only instantiation also works