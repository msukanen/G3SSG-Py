class ly:
    def __init__(self, val) -> None:
        self.val = val
    def __str__(self) -> str:
        return f'{self.val} ly'
    def __repr__(self) -> str:
        return f'ly(val={self.val})'
