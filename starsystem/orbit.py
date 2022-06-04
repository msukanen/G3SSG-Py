import enum
from star import Star
from dice import d6

class EmptyOrbit:
    def __init__(self) -> None:
        pass

class Terrestrial:
    def __init__(self, star:Star) -> None:
        pass

class AsteroidBelt:
    class Type(enum.Enum):
        M = 0
        S = 1
        C = 2
        def __str__(self) -> str:
            return f'{self.name}-type'
    def __init__(self, fixed = None) -> None:
        if fixed == None:
            self.__initR__()
        else:
            self.__type = fixed.__type
            self.__icy = fixed.__icy
            self.__vla = fixed.__vla
    def __initR__(self) -> None:
        self.__icy = False
        accepted = False
        while not accepted:
            accepted = True
            r = d6(3)
            if r < 5: self.__type = AsteroidBelt.Type.M
            elif r < 14: self.__type = AsteroidBelt.Type.S
            elif r < 18: self.__type = AsteroidBelt.Type.C
            else:
                accepted = False
                self.__icy = True
        self.__vla = d6(5) == 5
    def __str__(self) -> str:
        if self.__icy: return f'icy {self.__type}'
        else:          return f'{self.__type}'
    def icy(self) -> bool:
        return self.__icy
    def type(self):
        return self.__type
    def hasVeryLargeAsteroids(self) -> bool:
        return self.__vla

class GasGiant:
    class Size(enum.Enum):
        Small = 0
        Medium = 1
        Large = 2
        Huge = 3
    def __init__(self, star:Star, size:Size = None) -> None:
        pass

class Orbit:
    def __init__(self, star:Star, index:int, what = None) -> None:
        self.__index = index
        if what == None:
            self.__initR__(star)
        else: self.__what = what
    def __initR__(self, star:Star) -> None:
        if star.isOrbitClose(self.__index):
            r = d6(2)
            if   r < 5:  self.__what = EmptyOrbit()
            elif r < 7:  self.__what = Terrestrial(star)
            elif r < 10: self.__what = Terrestrial(star)
            elif r < 12: self.__what = AsteroidBelt()
            elif self.__index > 1: self.__what = GasGiant(star, GasGiant.Size.Huge)
        elif star.isOrbitFar(self.__index):
            r = d6(1)
            if star.isOrbitFar(self.__index, 10):
                r += 1
            if   r == 1: self.__what = Terrestrial(star)
            elif r == 2: self.__what = AsteroidBelt()
            elif r == 3: self.__what = EmptyOrbit()
            elif r < 7:  self.__what = GasGiant(star)
            else:        self.__what = Terrestrial()
        else:
            r = d6(2)
            if r < 4:     self.__what = EmptyOrbit()
            elif r < 9:   self.__what = Terrestrial(star)
            elif r < 11:  self.__what = AsteroidBelt()
            elif r == 11: self.__what = GasGiant(star, GasGiant.Size.Large)
            else:         self.__what = GasGiant(star, GasGiant.Size.Huge)
