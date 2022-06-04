import random

def __anyD(num:int, x:int) -> int:
    """Roll `num` of `x`-sided dice.
    
    :param `num`: number of dice.
    :param `x`: sides per die."""
    if (num == 0) or (x == 0):
        return 0
    if (not isinstance(num, int)) or (not isinstance(x, int)):
        raise Exception("Sorry, dice rolling operates only with integers!")
    r = 0
    for _ in range(0, abs(num)):
        r += random.randint(1, abs(x))
    return r

def d6(num:int = 1) -> int:
    """Roll `num` D6's.
    
    :param `num`: number of dice."""
    return __anyD(num, 6)

def d10(num:int = 1) -> int:
    """Roll `num` D10's.
    
    :param `num`: number of dice."""
    return __anyD(num, 10)
