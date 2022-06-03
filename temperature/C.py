import numbers

class C:
    def __init__(self, val) -> None:
        self.val = val

    def __str__(self) -> str:
        return f'{self.val}°C'

    def __repr__(self) -> str:
        return f'C(val={self.val})'

    def __add__(self, other):
        return C(self.val + (toC(other)).val)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return C(self.val * other)
        raise Exception(f'Multiplication with {type(other)} is not supported!')

from .convert import toC
