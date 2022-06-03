class K:
    def __init__(self, val):
        self.val = val
    def __str__(self) -> str:
        return f'{self.val}K'
    def __repr__(self) -> str:
        return f'K(val={self.val})'
