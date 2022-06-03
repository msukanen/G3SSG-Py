from ast import Is
import re
from .C import C
from .K import K
from .F import F

def toC(v):
    if isinstance(v, C):
        return v
    if isinstance(v, K):
        return C(v.val - 273.15)
    if isinstance(v, F):
        return C((v.val - 32) * (5.0/9.0))
    raise(f"{toC.__qualname__} doesn't support 'v' of {type(v)}")

def toK(v):
    if isinstance(v, C):
        return K(v.val + 273.15)
    if isinstance(v, K):
        return v
    if isinstance(v, F):
        return toK(toC(v))
    raise(f"{toK.__qualname__} doesn't support 'v' of {type(v)}")

def toF(v):
    if isinstance(v, C):
        return F((v.val * (9.0/5.0)) + 32)
    if isinstance(v, K):
        return toF(toC(v))
    if isinstance(v, F):
        return v
    raise(f"{toF.__qualname__} doesn't support 'v' of {type(v)}")
