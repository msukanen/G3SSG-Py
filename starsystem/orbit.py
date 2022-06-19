import enum
import numbers
from telnetlib import GA
from star import Star
from dice import d6
import random
from distance import mi
from indict import dictInc

__EARTH_RAD = mi(7915) / 2
__EARTH_DNS = 5.5

def __gravityFor(r:float, d:float) -> float:
    """Determine gravity from given radius and density.
    
    :param `r`: radius of planet.
    :param `d`: density of planet."""
    return (r/__EARTH_RAD) * (d/__EARTH_DNS)

class AxialTilt:
    class SeasonalEffect(enum.Enum):
        NoSeasons = 0
        Minor = 1
        EarthLike = 2
        Major = 3
        Gross = 4
    def __init__(self, fixed = None) -> None:
        if fixed == None:
            r = d6(2)
            if r < 4: self.__tilt = 0
            elif r < 8: self.__tilt = d6()*3
            elif r < 11: self.__tilt = d6(2)+20
            elif r == 11: self.__tilt = d6(3)+30
            else: self.__tilt = min(90, d6()*10+40)
            self.__seasonalEffect = self.__mkEff()
        elif isinstance(fixed, numbers.Number):
            self.__tilt = fixed
            self.__seasonalEffect = self.__mkEff()
        elif isinstance(fixed, AxialTilt):
            self.__tilt = fixed.__tilt
            self.__seasonalEffect = fixed.__seasonalEffect
        else: raise Exception(f'No idea how to convert {type(fixed)} into axial tilt...')
    def __mkEff(self):
        if   self.__tilt <  3: return AxialTilt.SeasonalEffect.NoSeasons
        elif self.__tilt < 19: return AxialTilt.SeasonalEffect.Minor
        elif self.__tilt < 33: return AxialTilt.SeasonalEffect.EarthLike
        elif self.__tilt < 50: return AxialTilt.SeasonalEffect.Major
        else:                  return AxialTilt.SeasonalEffect.Gross

class EmptyOrbit:
    def __init__(self) -> None:
        pass

class Moon:
    class Type(enum.Enum):
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

class Terrestrial:
    def __init__(self, star:Star) -> None:
        pass

class AsteroidBelt:
    """Encapsulate asteroid belt info."""
    class Type(enum.Enum):
        """Asteroid types."""
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
            if   r < 5:  self.__type = AsteroidBelt.Type.M
            elif r < 14: self.__type = AsteroidBelt.Type.S
            elif r < 18: self.__type = AsteroidBelt.Type.C
            else:
                accepted = False
                self.__icy = True
        self.__vla = d6(5) == 5
    def __str__(self) -> str:
        if self.__icy: return f'icy {self.__type}'
        else:          return f'{self.__type}'
    @property
    def icy(self) -> bool:
        """Asteroid belt is icy?"""
        return self.__icy
    @property
    def type(self):
        """Get type of asteroids in the belt."""
        return self.__type
    @property
    def hasVeryLargeAsteroids(self) -> bool:
        """Does the belt have very large asteroid(s) (akin to Vesta, Ceres, etc.)?"""
        return self.__vla

class GasGiant:
    """Encapsulate Gas Giant info."""
    class Size(enum.Enum):
        """Gas giant size categories."""
        Small = 0
        Medium = 1
        Large = 2
        Huge = 3
    class SpecialFeature(enum.Enum):
        """Gas giant special features."""
        RetrogradeMoon = 0,
        InclinedOrbitMoon = 1,
        FaintRing = 2,
        SpectacularRing = 3,
        AsteroidBelt = 4,
        OortBelt = 5,
        HabitableMoon = 6
    def __init__(self, star:Star, fixed = None) -> None:
        if fixed == None:
            self.__initR__()
        elif isinstance(fixed, GasGiant.Size):
            self.__initR__(star, fixed)
        else:
            self.__size = fixed.__size
            self.__radius = fixed.__radius
            self.__dow = fixed.__dow
            self.__density = fixed.__density
            self.__gravity = fixed.__gravity
            self.__axtilt = fixed.__axtilt
            self.__moons = fixed.__moons
            self.__sfeats = fixed.__sfeats
    def __initR__(self, star:Star, size:Size = None):
        if size == None:
            self.__dow = False
            accepted = False
            match star.klass():
                case Star.Class.M:
                    mod = -2
                    canBeH = False
                case Star.Class.K:
                    mod = -1
                    canBeH = False
                case _:
                    mod = 0
                    canBeH = True
            while not accepted:
                accepted = True
                r = d6(3)
                if (r < 4) and canBeH:
                    self.__size = GasGiant.Size.Huge
                    self.__dow = True
                elif r < 4:
                    canBeH = True
                    accepted = False
                elif (r == 4) and canBeH:
                    self.__size = GasGiant.Size.Huge
                elif r == 4:
                    canBeH = True
                    accepted = False
                elif r < 9:
                    self.__size = GasGiant.Size.Small
                elif r <= 13:
                    self.__size = GasGiant.Size.Medium
                else:
                    self.__size = GasGiant.Size.Large
        match self.__size:
            case GasGiant.Size.Small:
                self.__radius = random.uniform(27000.0, 33000.0, 1)
            case GasGiant.Size.Medium:
                self.__radius = random.uniform(45000.0, 55000.0, 1)
            case GasGiant.Size.Large:
                self.__radius = random.uniform(72000.0, 88000.0, 1)
            case _:
                self.__radius = random.uniform(180000.0, 220000.0, 1)
        self.__density = random.uniform(0.6, 2.5, 1)
        self.__gravity = __gravityFor(self.__radius, self.__density)
        self.__axtilt = AxialTilt()
        match self.__size:
            case GasGiant.Size.Large: mod = 1
            case GasGiant.Size.Huge: mod = 2
            case _: mod = 0
        self.__moons = {}
        self.__moons[Moon.Type.Moonlet] = Moon(Moon.Type.Moonlet, d6(3)+mod)
        self.__moons[Moon.Type.Small] = Moon(Moon.Type.Small, d6(2)+mod)
        self.__moons[Moon.Type.Medium] = Moon(Moon.Type.Medium, d6()+1+mod)
        n = d6()-3+mod
        if n > 0: self.__moons[Moon.Type.Large] = Moon(Moon.Type.Large, n)
        n = d6()-5+mod
        if n > 0: self.__moons[Moon.Type.Giant] = Moon(Moon.Type.Giant, n)
        n = d6()-7+mod
        if n > 0:
            ggs = []
            for _ in range(0,n):
                ggs.append(GasGiant(star, GasGiant.Size.Small))
            self.__moons[Moon.Type.SmallGG] = ggs
        match self.__size:
            case GasGiant.Size.Huge: mod = 3
            case GasGiant.Size.Large: mod = 2
            case _: mod = 0
        self.__sfeats = {}
        accepted = 1
        while accepted > 0:
            accepted -= 1
            r = d6(3)+mod
            if r < 10: pass
            elif r == 10 and d6()<4: dictInc(self.__sfeats, GasGiant.SpecialFeature.RetrogradeMoon)
            elif r == 10: dictInc(self.__sfeats, GasGiant.SpecialFeature.InclinedOrbitMoon)
            elif r < 14: dictInc(self.__sfeats, GasGiant.SpecialFeature.FaintRing)
            elif r == 14: dictInc(self.__sfeats, GasGiant.SpecialFeature.SpectacularRing)
            elif r == 15: dictInc(self.__sfeats, GasGiant.SpecialFeature.AsteroidBelt)
            elif r == 16: dictInc(self.__sfeats, GasGiant.SpecialFeature.OortBelt)
            elif r == 17:
                for m in self.__moons: m.number *= 2
            elif r == 18: accepted += 2
            else: dictInc(self.__sfeats, GasGiant.SpecialFeature.HabitableMoon)

    def size(self) -> Size:
        """Get size category."""
        return self.__size
    def radius(self) -> float:
        """Get radius (in one or other suitable unit)."""
        return self.__radius
    def density(self) -> float:
        """Get density value."""
        return self.__density
    def gravity(self) -> float:
        """Get gravity in Gs."""
        return self.__gravity
    def destroyerOfWorlds(self) -> bool:
        """Is this giant a 'destroyer of worlds'?"""
        return self.__dow
    def axialTilt(self) -> AxialTilt:
        """Get axial tilt."""
        return self.__axtilt

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
