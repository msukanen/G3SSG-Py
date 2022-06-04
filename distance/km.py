import numbers

class km:
    def __init__(self, val) -> None:
        if isinstance(val, km):
            self.val = val.val
        elif isinstance(val, numbers.Number):
            self.val = val
        else:
            self.val = toKM(val).val

    def __str__(self) -> str:
        return f'{self.val} km'

    def __repl__(self) -> str:
        return f'km(val={self.val})'

    def __plus__(self, other):
        return km(self.val + (toKM(other)).val)
        
    def __mul__(self, other):
        return km(self.val * (toKM(other)).val)

from .convert import toKM
