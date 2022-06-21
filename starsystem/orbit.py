from star import Star
from dice import d6
from .asteroidbelt import AsteroidBelt
from .moons import Moon
from .density import Density
from .gasgiant import GasGiant
from .planet import Planet

class EmptyOrbit:
    def __init__(self) -> None:
        pass

class Terrestrial(Planet):
    """Encapsulate more or less 'terrestrial' planet."""
    def __init__(self, star:Star, oid:int) -> None:
        super().__init__(star, oid)
        self._density = Density()

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
    @property
    def what(self):
        return self.__what
