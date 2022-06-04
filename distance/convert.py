import numbers

def toKM(v):
    """Convert v to kilometers.
    
    :param `v`: some distance value."""
    if isinstance(v, AU):
        return km(v.val * 149597870.691)
    if isinstance(v, ly):
        return toKM(toAU(v))
    if isinstance(v, pc):
        return toKM(toLY(v))
    if isinstance(v, mi):
        return km(v.val * 1.60934)
    if isinstance(v, km):
        return v
    if isinstance(v, numbers.Number):
        return km(v)
    raise Exception(f"{toKM.__qualname__} doesn't support 'v' of {type(v)}")

def toMI(v):
    """Convert v to miles.
    
    :param `v`: some distance value."""
    if isinstance(v, AU):
        return toMI(toKM(v))
    if isinstance(v, ly):
        return toMI(toKM(v))
    if isinstance(v, pc):
        return toMI(toKM(v))
    if isinstance(v, mi):
        return v
    if isinstance(v, km):
        return mi(v.val / 1.60934)
    raise Exception(f"{toMI.__qualname__} doesn't support 'v' of {type(v)}")

def toAU(v):
    """Convert v to AU (astronomical units).
    
    :param `v`: some distance value."""
    if isinstance(v, AU):
        return v
    if isinstance(v, ly):
        return AU(v.val * 63241.077088071)
    if isinstance(v, pc):
        return toAU(toLY(v))
    if isinstance(v, mi):
        return toAU(toKM(v))
    if isinstance(v, km):
        return km(v.val / 149597870.691)
    if isinstance(v, numbers.Number):
        return AU(v)
    raise Exception(f"{toAU.__qualname__} doesn't support 'v' of {type(v)}")

def toLY(v):
    """Convert v to ly (light years).
    
    :param `v`: some distance value."""
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
    """Convert v to pc (parsecs).
    
    :param `v`: some distance value."""
    if isinstance(v, AU):
        return toPC(toLY(v))
    if isinstance(v, ly):
        return pc(v.val / 3.26156)
    if isinstance(v, pc):
        return v
    if isinstance(v, km):
        return toPC(toLY(v))
    if isinstance(v, mi):
        return toPC(toKM(v))
    if isinstance(v, numbers.Number):
        return pc(v)
    raise Exception(f"{toPC.__qualname__} doesn't support 'v' of {type(v)}")

from .AU import AU
from .ly import ly
from .pc import pc
from .km import km
from .mi import mi
