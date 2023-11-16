from os import name
from importlib import import_module

# 动态导入操作系统相关模块
globals().update(import_module(f'.{name}', __package__).__dict__)

'''
if os.name == 'nt':
    # 导入 Windows 相关模块
    from . import nt
    globals().update(nt.__dict__)
else:
    # 导入 POSIX 相关模块
    from . import posix
    globals().update(posix.__dict__)
'''
