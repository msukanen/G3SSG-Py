import numbers

class mi:
    def __init__(self, val) -> None:
        if isinstance(val, mi):
            self.val = val.val
        elif isinstance(val, numbers.Number):
            self.val = val
        else:
            self.val = toMI(val).val

    def __str__(self) -> str:
        return f'{self.val} mi'

    def __repl__(self) -> str:
        return f'mi(val={self.val})'

    def __plus__(self, other):
        return mi(self.val + (toMI(other)).val)
        
    def __mul__(self, other):
        return mi(self.val * (toMI(other)).val)

from .convert import toMI
