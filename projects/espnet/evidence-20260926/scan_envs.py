import glob, subprocess, os, sys

cands = sorted(glob.glob("/opt/miniconda/envs/*/bin/python")) + ["/opt/miniconda/bin/python"]
code = (
    "import torch, importlib.util\n"
    "print('  torch', torch.__version__)\n"
    "print('  has torch.accelerator', hasattr(torch, 'accelerator'))\n"
    "try:\n"
    "    from torch import accelerator as A\n"
    "    print('  accelerator.is_available()', A.is_available())\n"
    "    print('  current_accelerator()', A.current_accelerator())\n"
    "except Exception as e:\n"
    "    print('  accelerator ERR', type(e).__name__, e)\n"
    "print('  cuda.is_available()', torch.cuda.is_available())\n"
    "print('  dist.is_available()', torch.distributed.is_available())\n"
    "print('  dist.is_gloo_available()', torch.distributed.is_gloo_available())\n"
    "print('  has torch_npu', importlib.util.find_spec('torch_npu') is not None)\n"
    "print('  has espnet', importlib.util.find_spec('espnet') is not None)\n"
)
for p in cands:
    if not os.path.exists(p):
        continue
    print("=== %s ===" % p)
    r = subprocess.run([p, "-c", code], capture_output=True, text=True, timeout=120)
    out = (r.stdout + r.stderr).strip()
    print(out[:1200] if out else "(no output)")
