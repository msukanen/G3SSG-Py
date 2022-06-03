import numbers

class F:
    def __init__(self, val) -> None:
        self.val = val

    def __str__(self) -> str:
        return f'{self.val}°F'

    def __repr__(self) -> str:
        return f'F(val={self.val})'

    def __add__(self, other):
        return F(self.val + (toF(other)).val)
        
    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return F(self.val * other)
        raise Exception(f'Multiplication with {type(other)} is not supported!')

from .convert import toF
