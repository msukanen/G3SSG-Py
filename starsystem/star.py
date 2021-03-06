from enum import Enum
from typing import Type
from dice import d6, d10
from distance import *
import random

class Star:
    """Encapsulates all kinds of star-related info.
    
    NOTE: this class is meant to be "immutable". Afterall, stars seldom change their
    parameters, and when/if they do it'll be rather spectacular...
    """
    class Type(Enum):
        """
        Star types (size categories).
        
        SEE: https://en.wikipedia.org/wiki/Stellar_classification
        """
        D = 0 # also 'VII'
        sd = 1 # also 'VI'
        V = 2
        IV = 3
        III = 4
        II = 5
        Ib = 6
        Iab = 7 # intermediate superg
        Ia = 7
        Iap = 8 # Ia+ hyperg
        def __str__(self) -> str:
            return self.name
    class Class(Enum):
        """
        Star class (color).
                
        SEE: https://en.wikipedia.org/wiki/Stellar_classification
        """
        D = 0
        T = 1
        L = 2
        M = 3
        K = 4
        G = 5
        F = 6
        A = 7
        B = 8
        O = 9
        def __str__(self) -> str:
            return self.name
    def __init__(self, fixed = None) -> None:
        """Construct self either based on other star (aka. 'fixed') or completely randomly."""
        if isinstance(fixed, Star):
            self.__size = fixed.__size
            self.__type = fixed.__type
            self.__mass = fixed.__mass
            self.__biozone = fixed.__biozone
            self.__innerLimit = fixed.__innerLimit
            self.__radius = fixed.__radius
            self.__numOrbits = fixed.__numOrbits
            self.__lrm = fixed.__lrm
            self.__bodec = fixed.__bodec
            self.__based = fixed.__based
            self.__luminosity = fixed.__luminosity
        else:
            self.__initR__()
    def __initR__(self):
        """Randomized construction of a star."""
        r = d6(3)
        if r < 6:
            sz = Star.Type.V
        elif r == 6:
            sz = Star.Type.sd
        elif r < 18:
            sz = Star.Type.V
        else:
            r = d6(3)
            if r == 3:
                r = d6(1)
                if r < 3:
                    sz = Star.Type.Ia
                else:
                    sz = Star.Type.Ib
            elif r == 4: sz = Star.Type.II
            elif r < 13: sz = Star.Type.III
            else:        sz = Star.Type.IV
        # determine type 2nd
        if sz == Star.Type.V:
            match d6(3):
                case 3: ty = Star.Class.O
                case 4: ty = Star.Class.B
                case 5: ty = Star.Class.A
                case 6: ty = Star.Class.F
                case 7: ty = Star.Class.G
                case 8: ty = Star.Class.K
                case _: ty = Star.Class.M
        elif sz == Star.Type.sd:
            match d6():
                case 1: ty = Star.Class.G
                case 2: ty = Star.Class.K
                case _: ty = Star.Class.M
        elif sz == Star.Type.D:
            ty = Star.Class.D
        else:
            accepted = False
            while not accepted:
                accepted = True
                r = d6(2)
                if r == 2:
                    if sz == Star.Type.II or sz == Star.Type.III or sz == Star.Type.IV:
                        accepted = False
                    else:    ty = Star.Class.O
                elif r == 3:
                    if sz == Star.Type.IV:
                        accepted = False
                    else:    ty = Star.Class.M
                elif r < 6:  ty = Star.Class.B
                elif r < 10: ty = Star.Class.K
                else:        ty = Star.Class.A
        usz = sz
        uty = ty
        if sz == Star.Type.D:
            while True:
                ost = Star()
                if ost.size is not Star.Type.D:
                    break
            usz = ost.size
            uty = ost.type
        else:
            usz = sz
            uty = ty
        dta  = Star.__genDtaBy(sz, ty)
        if sz == Star.Type.D:
            udta = Star.__genDtaBy(usz, uty)
        print(dta)
        self.__size = sz
        self.__type = ty
        self.__mass = dta[0]
        self.__biozone = dta[1]
        self.__innerLimit = AU(dta[2])
        self.__radius = AU(dta[3])
        if sz == Star.Type.D:
            porb = udta[4]
            norb = udta[5]
        else:
            porb = dta[4]
            norb = dta[5]
        self.__numOrbits = 0 if d6(3)>porb else norb
        self.__lrm = dta[6]
        self.__based = AU(0.1*d6(1))
        if (sz == Star.Type.sd) and (sz == Star.Class.M):
            self.__bodec = random.uniform(0.195, 0.205)
        else:
            self.__bodec = random.uniform(0.3, 0.4)
        self.__luminosity = d10(1)-1

    @property
    def type(self):
        """Get star's size category."""
        return self.__size
    @property
    def klass(self):
        """Get star's type (color)."""
        return self.__type
    @property
    def mass(self) -> float:
        """Get star's stellar mass in relation to Sol (e.g. Sol ??? 1.0)."""
        return self.__mass
    @property
    def biozone(self) -> tuple[AU, AU]:
        """
        Get star's biozone (goldilocks zone) borders.

        :returns: tuple(...)
            - inner limit in AU
            - outer limit in AU
        """
        if isinstance(self.__biozone, AU):
            return self.__biozone, self.__biozone*1.5
        else: return self.__biozone[0], self.__biozone[1]
    def isOrbitClose(self, orbitIdx) -> bool:
        """
        Determine whether given orbit is closer than [Goldilocks zone](https://en.wikipedia.org/wiki/Circumstellar_habitable_zone).

        :param orbitIdx: index
        """
        return self.distanceOf(orbitIdx) < self.biozone()[0]
    def isOrbitFar(self, orbitIdx:int, by:int = 1) -> bool:
        """
        Determine whether given orbit is further out than [Goldilocks zone](https://en.wikipedia.org/wiki/Circumstellar_habitable_zone).

        :param `orbitIdx`: `0+`-index
        :param `by`: desired border distance multiplier, if any; default: `1`
        """
        return (self.distanceOf(orbitIdx) * by) > self.biozone()[1]
    @property
    def innerLimit(self) -> AU:
        """Get star's inner limit.
        
        Below this limit no solid matter can exist for long. It either evaporates or is sucked into the star itself."""
        return self.__innerLimit
    def canOrbitExist(self, orbitIdx:int) -> bool:
        """See if given orbit can hold anything permanent.
        
        See also: `innerLimit()`"""
        return self.distanceOf(orbitIdx) > self.innerLimit()
    @property
    def radius(self) -> AU:
        """Get radius of the star."""
        return self.__radius
    @property
    def numOrbits(self) -> int:
        """Get number of potential orbits."""
        return self.__numOrbits
    @property
    def lifeRollMod(self) -> int:
        """Get star's life roll modifier."""
        return self.__lrm
    def distanceOf(self, orbitIdx:int) -> AU:
        """Determine distance of the given orbit.
        
        :param `orbitIdx`: `0+`-index"""
        if orbitIdx == 0:
            return self.__based
        elif orbitIdx == 1:
            return self.__based + self.__bodec
        else:
            return self.__based + pow(2, orbitIdx-1) * self.__bodec
    @property
    def luminosity(self) -> int:
        """Get star's luminosity.
        
        Luminosity ranges from 0 (brightest) to 9 (dimmest)."""
        return self.__luminosity
    def __str__(self) -> str:
        if self.__type == Star.Type.D:
            return 'D'
        return f'{self.__type}{self.__luminosity}{self.__size}'
    @staticmethod
    def __genDtaBy(s:Type, c:Class) -> tuple[float, AU, AU, AU, int, int, int]:
        """
        Choose star data based on its size and type.

        :param `s`: Star type (size).
        :param `c`: Star class (color).
        :returns: tuple(...)
            - stellar mass
            - biozone - AU, or a tuple of inner AU and outer AU
            - inner limit
            - radius
            - potential of planets on 3d6
            - number of orbits to determine if/when orbital potential is fulfilled
            - life roll mod
        """
        if c is Star.Class.O:
            if   s is Star.Type.Ia: return 70, AU(790), AU(16), AU(0.2), 0, None, -12
            elif s is Star.Type.Ib: return 60, AU(630), AU(13), AU(0.1), 0, None, -12
            else:                   return 50, AU(500), AU(10), 0, None, -9
        elif c is Star.Class.B:
            if   s is Star.Type.Ia: return 50, AU(500), AU(10), AU(0.2), 0, None, -10
            elif s is Star.Type.Ib: return 40, AU(320), AU(6.3), AU(0.1), 0, None, -10
            elif s is Star.Type.II: return 35, AU(250), AU(5), AU(0.1), 3, d6(3)+1, -10
            elif s is Star.Type.III: return 30, AU(200), AU(4), 0, 3, d6(3)+1, -10
            elif s is Star.Type.IV: return 20, AU(180), AU(3.8), 0, 3, d6(3)+1, -10
            else:                   return 10, AU(30), AU(0.6), 0, 4, d6(3), -9
        elif c is Star.Class.A:
            if   s is Star.Type.Ia: return 30, AU(200), AU(4), AU(0.6), 3, d6(3)+3, -10
            elif s is Star.Type.Ib: return 16, AU(50), AU(1), AU(0.2), 3, d6(3)+2, -10
            elif s is Star.Type.II: return 10, AU(20), AU(0.4), 0, 3, d6(3)+2, -10
            elif s is Star.Type.III: return 6, AU(5), 0, 0, 3, d6(3)+1, -10
            elif s is Star.Type.IV: return 4, AU(4), 0, 0, 4, d6(3), -10
            else:                   return 3, AU(3.1), 0, 0, 5, d6(3)-1, -9
        elif c is Star.Class.F:
            if   s is Star.Type.Ia: return 15, AU(200), AU(4), AU(0.8), 4, d6(3)+3, -10
            elif s is Star.Type.Ib: return 13, AU(50), AU(1), AU(0.2), 4, d6(3)+2, -10
            elif s is Star.Type.II: return 8, AU(13), AU(0.3), 0, 4, d6(3)+1, -9
            elif s is Star.Type.III: return 2.5, AU(2.5), AU(0.1), 0, 4, d6(3), -9
            elif s is Star.Type.IV: return 2.2, AU(2), 0, 0, 6, d6(3), -9
            else:                   return 1.9, AU(1.6), 0, 0, 13, d6(3)-1, -8
        elif c is Star.Class.G:
            if   s is Star.Type.Ia: return 12, AU(160), AU(3.1), AU(1.4), 6, d6(3)+3, -10
            elif s is Star.Type.Ib: return 10, AU(50), AU(1), AU(0.4), 6, d6(3)+2, -10
            elif s is Star.Type.II: return 6, AU(13), AU(0.3), AU(0.1), 6, d6(3)+1, -9
            elif s is Star.Type.III: return 2.7, AU(3.1), AU(0.1), 0, 6, d6(3), -8
            elif s is Star.Type.IV: return 1.8, AU(1), 0, 0, 7, d6(3)-1, -6
            elif s is Star.Type.V: return 1.1, AU(0.8), 0, 0, 16, d6(3)-2, 0
            else:                  return 0.8, AU(0.5), 0, 0, 16, d6(2)+1, 1
        elif c is Star.Class.K:
            if   s is Star.Type.Ia: return 15, AU(125), AU(2.5), AU(3), 10, d6(3)+2, -10
            elif s is Star.Type.Ib: return 12, AU(50), AU(1), AU(1), 16, d6(3)+2, -10
            elif s is Star.Type.II: return 6, AU(13), AU(0.3), AU(0.2), 16, d6(3)+1, -9
            elif s is Star.Type.III: return 3, AU(4), AU(0.1), 0, 16, d6(3), -7
            elif s is Star.Type.IV: return 2.3, AU(1), 0, 0, 16, d6(3)-1, -5
            elif s is Star.Type.V: return 0.9, (AU(0.5), AU(0.6)), 0, 0, 16, d6(3)-2, 0
            else:                  return 0.5, AU(0.2), 0, 0, 16, d6(2)+1, 1
        elif c is Star.Class.M:
            if   s is Star.Type.Ia: return 20, AU(100), AU(2), AU(7), 16, d6(3), -10
            elif s is Star.Type.Ib: return 16, AU(50), AU(1), AU(4.2), 16, d6(3), -10
            elif s is Star.Type.II: return 8, AU(16), AU(0.3), AU(1.1), 16, d6(3), -9
            elif s is Star.Type.III: return 4, AU(5), AU(0.1), AU(0.3), 16, d6(3), -6
            elif s is Star.Type.V: return 0.3, (AU(0.1), AU(0.2)), 0, 0, 16, d6(3)-2, 1
            else:                  return 0.2, (AU(0.1), AU(0.1)), 0, 0, 16, d6(2)+2, 2
        else:
            return 0.8, (AU(0.03), AU(0.03)), 0, 0, 0, 0, -10
