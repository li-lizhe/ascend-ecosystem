"""测试用最小桩：fcntl 是 POSIX-only 模块，Windows 上没有。

speculators/data_generation/vllm_client.py 在 import 期 `import fcntl`，并用
`fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)` 做跨进程文件锁。被测控制流
（render endpoint 失败的分类/中止）不涉及该锁，故此处做成 no-op。
"""

LOCK_SH = 1
LOCK_EX = 2
LOCK_NB = 4
LOCK_UN = 8
LOCK_MAND = 32


def flock(fd, operation):  # noqa: ARG001 - 桩：永远视为加锁成功
    return None


def lockf(fd, cmd, len=0, start=0, whence=0):  # noqa: ARG001
    return None
