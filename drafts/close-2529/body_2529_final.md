## 复核结论：这是旧构建的问题，新版已修复

感谢跟进。我们回查后确认，我们报的现象**出在我们当时使用的过期构建**上，较新的构建已不复现。

### 1、我们复现时的构建

包版本 `triton_ascend-3.6.0+git0cfb1708`（提交 `0cfb1708`，2026-08-05）。该版本的
`third_party/ascend/backend/driver.py` 取 kernel_name 是：

```c
PyObject *kernelNameObj = PyDict_GetItemString(packedMetadata, "kernel_name");
const char *kernelName = PyUnicode_AsUTF8(kernelNameObj);
```

取不到时返回空指针，下一行直接解引用 → segfault，即本 issue 报的现象。

### 2、机制在真机上坐实

Ascend 910B2 / CANN 9.2.0-beta.2 上直接调用 launcher 的 C 层 `launch`
（13 个参数，第 6 个为 packedMetadata），**只改第 6 个参数的类型**，其余参数完全相同：

| 第 6 个参数 | 结果 |
|---|---|
| 真 dict | `RETURNED None`（正常） |
| `KernelMetadata`（namedtuple） | `EXIT=139`，Segmentation fault (core dumped) |

### 3、新版不再崩

自 **#1651（merged 2026-08-21）** 起，同样两行改为 `PyDict_GetItemWithError` + 判空，
取不到时抛 `KeyError: "packedMetadata missing 'kernel_name'"`。

我们在新版栈（torch `5eb6d3d` / torch_npu `b968b45` / triton_ascend `38945468`）上
用**同一份脚本**复跑同一输入：结果 `KeyError`、`EXIT=0`，进程存活。

### 结论

本 issue 为**旧构建问题**，升级到含 #1651 的构建即已修复。感谢排查。
