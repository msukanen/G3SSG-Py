class F:
    def __init__(self, val) -> None:
        self.val = val
    def __str__(self) -> str:
        return f'{self.val}°F'
    def __repr__(self) -> str:
        return f'F(val={self.val})'
