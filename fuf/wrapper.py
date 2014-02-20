#!/usr/bin/env python
"""
Action Set class and demonstration
Matt Soucy

The main purpose of this file is to demonstrate some of the fun things
that can be done with functions in Python.

Particularly interesting are:
- `wrapper`: Duplicates a function perfectly down to the signature
   that is stored internally and printed with using help()
- `wwrapper`: Wrapper wrapper - apply as a decorator to a decorator to produce
   a decorator that generates perfect-forwarded functions
- `ActionSet().__call__`: uses magic for wrapping a function and hiding metadata
- `ActionSet`: Shows how easy it can be to inherit from `dict`

Ideas taken from:
- http://numericalrecipes.wordpress.com/2009/05/25/signature-preserving-function-decorators/
- http://github.com/msoucy/RepBot
"""
import inspect  # Used to create our duplicate
from functools import update_wrapper  # Convenience to update the metadata
from .interop import *


def wwrapper(_wrap_):
    '''Wrap a decorator with support for the perfect wrapper decorator'''
    def wrapper(_func_):
        '''Create a perfect wrapper (including signature) around a function'''
        # convert bar(f)(*args, **kwargs)
        # into    f(*args, **kwargs)
        src = r'def {0}{1}: return _wrap_(func){1}'.format(
            _func_.__name__,
            inspect.formatargspec(*inspect.getargspec(_func_))
        )
        evaldict = {'_wrap_': _wrap_, 'func': _func_}
        exec_(src, evaldict)
        ret = evaldict[_func_.__name__]
        update_wrapper(ret, _func_)
        ret.__wrapped__ = _func_
        return ret
    return wrapper

wrapper = wwrapper((lambda func:(lambda *_a, **_kw: func(*_a, **_kw))))
