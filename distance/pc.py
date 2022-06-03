class pc:
    def __init__(self, val) -> None:
        self.val = val
    def __str__(self) -> str:
        return f'{self.val} pc'
    def __repr__(self) -> str:
        return f'pc(val={self.val})'
