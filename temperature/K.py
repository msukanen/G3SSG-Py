import numbers

class K:
    def __init__(self, val) -> None:
        self.val = val
    
    def __str__(self) -> str:
        return f'{self.val}K'
    
    def __repr__(self) -> str:
        return f'K(val={self.val})'

    def __add__(self, other):
        return K(self.val + (toK(other)).val)
        
    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return K(self.val * other)
        raise Exception(f'Multiplication with {type(other)} is not supported!')

from .convert import toK
