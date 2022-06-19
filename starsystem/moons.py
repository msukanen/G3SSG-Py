from enum import Enum

class Moon:
    class Type(Enum):
        """Moon types."""
        Moonlet = 0
        Small = 1
        Medium = 2
        Large = 3
        Giant = 4
        SmallGG = 5
    def __init__(self, typ:Type, num:int) -> None:
        self.__type = typ
        self.__num = num

    @property
    def number(self):
        return self.__num

    @number.setter
    def number(self, n:int):
        self.__num = 0 if n < 1 else n
        return self.__num
