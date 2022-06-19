from decimal import Decimal
from enum import Enum
import random
from dice import d6

class Density:
    class Category(Enum):
        GasGiant = 0
        Silicate = 1
        LowIron = 2
        MdIron = 3
        HiIron = 4
        Metallic = 5

    def __init__(self, *, category:Category = None):
        if category == None:
            self.__dns = d6(3)/10 + d6()
            self.__category = Density.__cat4dns(self.__dns)
        else:
            self.__category = category
            match category:
                case Density.Category.GasGiant: self.__dns = random.uniform(0.6, 2.5, 1)
                case Density.Category.Silicate: self.__dns = random.uniform(1.3, 3.05, 1)
                case Density.Category.LowIron: self.__dns = random.uniform(3.1, 4.55, 1)
                case Density.Category.MdIron: self.__dns = random.uniform(4.6, 6.05, 1)
                case Density.Category.HiIron: self.__dns = random.uniform(6.1, 7.05, 1)
                case _: self.__dns = random.uniform(7.1, 8, 1)

    @property
    def category(self):
        return self.__category

    @property
    def value(self):
        return self.__dns

    @staticmethod
    def __cat4dns(dns:float) -> Category:
        if dns < 3.1: return Density.Category.Silicate
        elif dns < 4.6: return Density.Category.LowIron
        elif dns < 6.1: return Density.Category.MdIron
        elif dns < 7.1: return Density.Category.HiIron
        return Density.Category.Metallic
