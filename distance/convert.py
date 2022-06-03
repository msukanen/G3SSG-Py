import numbers

def toAU(v):
    if isinstance(v, AU):
        return v
    if isinstance(v, ly):
        return AU(v.val * 63241.077088071)
    if isinstance(v, pc):
        return toAU(toLY(v))
    if isinstance(v, numbers.Number):
        return AU(v)
    raise Exception(f"{toAU.__qualname__} doesn't support 'v' of {type(v)}")

def toLY(v):
    if isinstance(v, AU):
        return ly(v.val / 63241.077088071)
    if isinstance(v, ly):
        return v
    if isinstance(v, pc):
        return ly(v.val * 3.26156)
    if isinstance(v, numbers.Number):
        return ly(v)
    raise Exception(f"{toLY.__qualname__} doesn't support 'v' of {type(v)}")

def toPC(v):
    if isinstance(v, AU):
        return toPC(toLY(v))
    if isinstance(v, ly):
        return pc(v.val / 3.26156)
    if isinstance(v, pc):
        return v
    if isinstance(v, numbers.Number):
        return pc(v)
    raise Exception(f"{toPC.__qualname__} doesn't support 'v' of {type(v)}")

from .AU import AU
from .ly import ly
from .pc import pc
