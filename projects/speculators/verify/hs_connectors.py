"""测试用最小桩：只提供 speculators 在 import 期会触碰到的名字。

本机（Windows，无 hs_connectors 可选依赖）跑 render 边界测试时，speculators/__init__
会一路 import 到 train/data.py，那里 `from hs_connectors import FileTransfer,
HiddenStatesTransfer`；而 hs_connectors 属于可选 extra、未安装。这里的类只是占位，
被测控制流（render endpoint 失败分类）完全不触碰它们。
"""


class _Stub:
    def __init__(self, *a, **kw):
        pass


class FileTransfer(_Stub):
    pass


class HiddenStatesTransfer(_Stub):
    pass


class HiddenStatesBackend(_Stub):
    pass


class FP8Transfer(_Stub):
    pass
