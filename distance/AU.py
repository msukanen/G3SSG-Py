class AU:
    def __init__(self, val) -> None:
        self.val = val
    def __str__(self) -> str:
        return f'{self.val} AU'
    def __repl__(self) -> str:
        return f'AU(val={self.val})'
