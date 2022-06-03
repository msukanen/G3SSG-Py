import numbers


class pc:
    def __init__(self, val) -> None:
        if isinstance(val, pc):
            self.val = val.val
        elif isinstance(val, numbers.Number):
            self.val = val
        else:
            self.val = toPC(val).val

    def __str__(self) -> str:
        return f'{self.val} pc'

    def __repr__(self) -> str:
        return f'pc(val={self.val})'

    def __mul__(self, other):
        return pc(self.val * toPC(other).val)
        
    def __add__(self, other):
        return pc(self.val + toPC(other).val)

from .convert import toPC
