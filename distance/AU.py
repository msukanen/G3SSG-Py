import numbers


class AU:
    def __init__(self, val) -> None:
        if isinstance(val, AU):
            self.val = val.val
        elif isinstance(val, numbers.Number):
            self.val = val
        else:
            self.val = toAU(val).val

    def __str__(self) -> str:
        return f'{self.val} AU'

    def __repl__(self) -> str:
        return f'AU(val={self.val})'

    def __plus__(self, other):
        return AU(self.val + (toAU(other)).val)
        
    def __mul__(self, other):
        return AU(self.val * (toAU(other)).val)

from .convert import toAU
