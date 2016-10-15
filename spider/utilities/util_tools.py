# _*_ coding: utf-8 _*_

"""
util_tools.py by xianhu
"""

import functools

__all__ = [
    "params_chack",
]


def params_chack(*types, **kwtypes):
    """
    check the parameters of a function, usage: @params_chack(int, str, (int, str), key1=list, key2=(list, tuple))
    """
    def _decoration(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            result = [isinstance(_param, _type) for _param, _type in zip(args, types)]
            assert all(result), "params_chack: invalid parameters in " + func.__name__
            result = [isinstance(kwargs[_param], kwtypes[_param]) for _param in kwargs if _param in kwtypes]
            assert all(result), "params_chack: invalid parameters in " + func.__name__
            return func(*args, **kwargs)
        return _inner
    return _decoration
