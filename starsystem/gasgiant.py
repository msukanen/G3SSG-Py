from star import Star
from indict import dictInc
from enum import Enum
from .planet import Planet
from dice import d6
from .moons import Moon
import random
from .density import Density

class GasGiant(Planet):
    """Encapsulate Gas Giant info."""
    class Size(Enum):
        """Gas giant size categories."""
        Small = 0
        Medium = 1
        Large = 2
        Huge = 3
    class SpecialFeature(Enum):
        """Gas giant special features."""
        RetrogradeMoon = 0,
        InclinedOrbitMoon = 1,
        FaintRing = 2,
        SpectacularRing = 3,
        AsteroidBelt = 4,
        OortBelt = 5,
        HabitableMoon = 6
    def __init__(self, star:Star, fixed = None) -> None:
        super().__init__()
        if fixed == None:
            self.__initR__(star)
        elif isinstance(fixed, GasGiant.Size):
            self.__initR__(star, fixed)
        else:
            self.__size = fixed.__size
            self._radius = fixed._radius
            self.__dow = fixed.__dow
            self._density = fixed._density
            self._axtilt = fixed._axtilt
            self._moons = fixed._moons
            self.__sfeats = fixed.__sfeats
            self._lod = fixed._lod
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
        # radius
        match self.__size:
            case GasGiant.Size.Small:
                self._radius = random.uniform(27000.0, 33000.0, 1)
            case GasGiant.Size.Medium:
                self._radius = random.uniform(45000.0, 55000.0, 1)
            case GasGiant.Size.Large:
                self._radius = random.uniform(72000.0, 88000.0, 1)
            case _:
                self._radius = random.uniform(180000.0, 220000.0, 1)
        self._density = Density(category = Density.Category.GasGiant)
        # moons
        match self.__size:
            case GasGiant.Size.Large: mod = 1
            case GasGiant.Size.Huge: mod = 2
            case _: mod = 0
        self._moons = {}
        self._moons[Moon.Type.Moonlet] = Moon(Moon.Type.Moonlet, d6(3)+mod)
        self._moons[Moon.Type.Small] = Moon(Moon.Type.Small, d6(2)+mod)
        self._moons[Moon.Type.Medium] = Moon(Moon.Type.Medium, d6()+1+mod)
        n = d6()-3+mod
        if n > 0: self._moons[Moon.Type.Large] = Moon(Moon.Type.Large, n)
        n = d6()-5+mod
        if n > 0: self._moons[Moon.Type.Giant] = Moon(Moon.Type.Giant, n)
        n = d6()-7+mod
        if n > 0:
            ggs = []
            for _ in range(0,n):
                ggs.append(GasGiant(star, GasGiant.Size.Small))
            self._moons[Moon.Type.SmallGG] = ggs
        # special features
        self.__sfeats = {}
        match self.__size:
            case GasGiant.Size.Huge: mod = 3
            case GasGiant.Size.Large: mod = 2
            case _: mod = 0
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

    @property
    def size(self) -> Size:
        """Get size category."""
        return self.__size
        
    @property
    def destroyerOfWorlds(self) -> bool:
        """Is this giant a 'destroyer of worlds'?"""
        return self.__dow

    @property
    def special_features(self) -> dict:
        """Get map of special features."""
        return self.__sfeats
