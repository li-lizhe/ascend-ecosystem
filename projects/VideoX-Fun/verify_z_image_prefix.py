"""Isolated reproduction of LoadZImageTransformerModel.loadmodel's key-space handling.

The converter (`convert_state_dict`) and the gate that decides whether to run it are
extracted *verbatim* from comfyui/z_image/nodes.py (no copy-paste retyping) and exec'd
against a synthetic ComfyUI-format checkpoint, with a stub tensor object whose only used
method is `.chunk(3)` so no torch / ComfyUI install is needed.

Run:  python verify_z_image_prefix.py
"""
import re
import textwrap

SRC = "comfyui/z_image/nodes.py"
text = open(SRC, encoding="utf-8").read().replace("\r\n", "\n")

# --- extract the nested convert_state_dict definition (verbatim) -------------
start = text.index("        def convert_state_dict(old_state_dict):")
rest = text[start:]
# it ends at the line "            return new_state_dict"
end = rest.index("            return new_state_dict") + len("            return new_state_dict")
fn_src = textwrap.dedent(rest[:end])

# --- extract the gate line (verbatim) ---------------------------------------
gate = [l for l in text.splitlines() if l.strip().startswith('if "x_embedder.weight" in')]
assert gate, "gate not found"
gate_stmt = gate[0].strip()

# --- extract the prefix-strip block that the fix adds (verbatim) ------------
strip_block = re.search(
    r'(_prefix = "model\.diffusion_model\."\n.*?items\(\)\})', text, re.S)
strip_src = re.sub(r"(?m)^ {8}", "", strip_block.group(1)) if strip_block else None


class FakeTensor:
    """Stands in for a torch tensor; only `.chunk(3)` is used by the converter."""
    def __init__(self, name):
        self.name = name
    def chunk(self, n, dim=0):
        assert n == 3, "converter only chunks qkv by 3"
        return [FakeTensor(f"{self.name}#{i}") for i in range(n)]


def run_gate_and_convert(state_dict, apply_strip):
    ns = {"transformer_state_dict": state_dict}
    if apply_strip and strip_src:
        exec(strip_src, ns)
        state_dict = ns["transformer_state_dict"]
    exec(fn_src, ns)
    convert_state_dict = ns["convert_state_dict"]
    gate_cond = gate_stmt.strip()[len("if "):].rstrip().rstrip(":")
    if eval(gate_cond, {}, {"transformer_state_dict": state_dict}):
        return convert_state_dict(state_dict)
    return state_dict


def build_bare():
    """A Z-Image checkpoint keyed the way the converter's gate expects (bare keys)."""
    keys = [
        "x_embedder.weight",
        "x_embedder.bias",
        "final_layer.weight",
        "layers.0.attention.q_norm.weight",
        "layers.0.attention.k_norm.weight",
        "layers.0.attention.out.weight",
        "layers.0.attention.qkv.weight",
        "layers.0.feed_forward.w1.weight",
        "context_refiner.0.attention.qkv.weight",
    ]
    return {k: FakeTensor(k) for k in keys}


def build_prefixed(bare, prefix="model.diffusion_model."):
    """The same checkpoint as ComfyUI-native `diffusion_models/*.safetensors` store it."""
    return {prefix + k: v for k, v in bare.items()}


def check(label, keys):
    expected = set(run_gate_and_convert(build_bare(), apply_strip=True).keys())
    got = set(keys)
    missing = sorted(expected - got)
    unexpected = sorted(got - expected)
    ok = not missing and not unexpected
    print(f"\n[{label}]\n  keys={len(got)}  prefix kept="
          f"{any(k.startswith('model.diffusion_model.') for k in got)}")
    print(f"  -> load_state_dict(strict=True): {'OK' if ok else 'RuntimeError'}")
    if not ok:
        print(f"     Missing key(s):    {missing[:3]}{' ...' if len(missing) > 3 else ''}")
        print(f"     Unexpected key(s): {unexpected[:3]}{' ...' if len(unexpected) > 3 else ''}")
    return ok


print("extracted converter (lines verbatim from %s):" % SRC)
print(textwrap.indent(fn_src, "    ")[:300] + " ...")
print("gate:", gate_stmt)
print("prefix-strip block present in file:", strip_src is not None)

prefixed = build_prefixed(build_bare())
before = check("BEFORE fix: ComfyUI-prefixed checkpoint, no prefix handling",
               run_gate_and_convert(dict(prefixed), apply_strip=False))
after = check("AFTER fix: same checkpoint with the prefix stripped first",
              run_gate_and_convert(dict(prefixed), apply_strip=True))
bare = check("REFERENCE: bare-key checkpoint (already worked)",
             run_gate_and_convert(build_bare(), apply_strip=False))

print("\nRESULT:", "PASS - fix converts the prefixed checkpoint to the expected key space"
      if (not before and after and bare) else "FAIL")
