import numbers


class ly:
    def __init__(self, val) -> None:
        if isinstance(val, ly):
            self.val = val.val
        elif isinstance(val, numbers.Number):
            self.val = val
        else:
            self.val = toLY(val).val

    def __str__(self) -> str:
        return f'{self.val} ly'

    def __repr__(self) -> str:
        return f'ly(val={self.val})'

    def __mul__(self, other):
        return ly(self.val * toLY(other).val)
        
    def __add__(self, other):
        return ly(self.val + toLY(other).val)

from .convert import toLY
