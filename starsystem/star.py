from enum import Enum
from typing import Type
from dice import d6, d10
from distance import *

class Star:
    """Encapsulates all kinds of star-related info.
    
    NOTE: this class is meant to be "immutable". Stars, afterall, seldom change their
    parameters...
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
        else:
            self.__initR__()
    def __initR__(self):
        # determine size 1st
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
            r = d6(3)
            if   r == 3: ty = Star.Class.O
            elif r == 4: ty = Star.Class.B
            elif r == 5: ty = Star.Class.A
            elif r == 6: ty = Star.Class.F
            elif r == 7: ty = Star.Class.G
            elif r == 8: ty = Star.Class.K
            else:        ty = Star.Class.M
        elif sz == Star.Type.sd:
            r = d6()
            if   r == 1: ty = Star.Class.G
            elif r == 2: ty = Star.Class.K
            else:        ty = Star.Class.M
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
            accepted = False
            while not accepted:
                ost = Star()
                if ost.size is not Star.Type.D:
                    accepted = True
            usz = ost.size
            uty = ost.type
        else:
            usz = sz
            uty = ty
        dta  = genDtaBy(sz, ty)
        if sz == Star.Type.D:
            udta = genDtaBy(usz, uty)
        self.__size = sz
        self.__type = ty
        self.__mass = dta[0]
        self.__biozone = dta[1]
        self.__innerLimit = AU(dta[2])
        self.__radius = AU(dta[3])
        if sz == Star.Type.D:
            self.__numOrbits = udta[4]
        else: self.__numOrbits = dta[4]
        self.__lrm = dta[5]
        self.__based = AU(0.1*d6(1))
        if (sz == Star.Type.sd) and (sz == Star.Class.M):
            self.__bodec = 0.2
        else:
            r = d6(1)
            if   r < 3: self.__bodec = 0.3
            elif r < 5: self.__bodec = 0.35
            else:       self.__bodec = 0.4
        self.__luminosity = d10(1)-1

    def size(self):
        """Get star's size category.
        
        :returns: Star.Size"""
        return self.__size
    def type(self):
        """Get star's type (color).
        
        :returns: Star.Type"""
        return self.__type
    def mass(self) -> float:
        """Get star's relative mass (in relation to Sol).
        
        :returns: float"""
        return self.__mass
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
    def innerLimit(self):
        """Get star's inner limit. Below this limit no permanent solid matter can form.
        
        :returns: AU"""
        return self.__innerLimit
    def radius(self):
        """Get radius of the star.
        
        :returns: AU"""
        return self.__radius
    def numOrbits(self) -> int:
        """Get number of potential orbits."""
        return self.__numOrbits
    def lifeRollMod(self) -> int:
        """Get star's life roll modifier."""
        return self.__lrm
    def distanceOf(self, orbitId:int):
        """Determine distance of given orbit index.
        
        :param orbitId int: orbit index
        :return: `AU`"""
        if orbitId == 0:
            return self.__based
        elif orbitId == 1:
            return self.__based + self.__bodec
        else:
            return self.__based + pow(2, orbitId-1) * self.__bodec
    def luminosity(self) -> int:
        """Get star's luminosity.
        
        Luminosity ranges from 0 (brightest) to 9 (dimmest).
        
        :returns: `0-9`"""
        return self.__luminosity
    def __str__(self) -> str:
        if self.__type == Star.Type.D:
            return 'D'
        return f'{self.__type}{self.__luminosity}{self.__size}'
        
def genDtaBy(s, t):
    """
    Choose star data based on its size and type.

    :param Star.Size s: Star size.
    :param Star.Type t: Star type (color).
    :returns: tuple(...)
        - mass - mass relative to Sol.
        - biozone - AU or tuple(inner AU, outer AU)
        - inner limit - AU limit below which all matter vapes
        - radius - star's radius in AU
        - potential of planets on 3d6
        - number of possible orbits
        - life roll mod
    """
    if t is Star.Class.O:
        if   s is Star.Type.Ia: return 70, AU(790), AU(16), AU(0.2), 0, None, -12
        elif s is Star.Type.Ib: return 60, AU(630), AU(13), AU(0.1), 0, None, -12
        else:                   return 50, AU(500), AU(10), 0, None, -9
    elif t is Star.Class.B:
        if   s is Star.Type.Ia: return 50, AU(500), AU(10), AU(0.2), 0, None, -10
        elif s is Star.Type.Ib: return 40, AU(320), AU(6.3), AU(0.1), 0, None, -10
        elif s is Star.Type.II: return 35, AU(250), AU(5), AU(0.1), 3, d6(3)+1, -10
        elif s is Star.Type.III: return 30, AU(200), AU(4), 0, 3, d6(3)+1, -10
        elif s is Star.Type.IV: return 20, AU(180), AU(3.8), 0, 3, d6(3)+1, -10
        else:                   return 10, AU(30), AU(0.6), 0, 4, d6(3), -9
    elif t is Star.Class.A:
        if   s is Star.Type.Ia: return 30, AU(200), AU(4), AU(0.6), 3, d6(3)+3, -10
        elif s is Star.Type.Ib: return 16, AU(50), AU(1), AU(0.2), 3, d6(3)+2, -10
        elif s is Star.Type.II: return 10, AU(20), AU(0.4), 0, 3, d6(3)+2, -10
        elif s is Star.Type.III: return 6, AU(5), 0, 0, 3, d6(3)+1, -10
        elif s is Star.Type.IV: return 4, AU(4), 0, 0, 4, d6(3), -10
        else:                   return 3, AU(3.1), 0, 0, 5, d6(3)-1, -9
    elif t is Star.Class.F:
        if   s is Star.Type.Ia: return 15, AU(200), AU(4), AU(0.8), 4, d6(3)+3, -10
        elif s is Star.Type.Ib: return 13, AU(50), AU(1), AU(0.2), 4, d6(3)+2, -10
        elif s is Star.Type.II: return 8, AU(13), AU(0.3), 0, 4, d6(3)+1, -9
        elif s is Star.Type.III: return 2.5, AU(2.5), AU(0.1), 0, 4, d6(3), -9
        elif s is Star.Type.IV: return 2.2, AU(2), 0, 0, 6, d6(3), -9
        else:                   return 1.9, AU(1.6), 0, 0, 13, d6(3)-1, -8
    elif t is Star.Class.G:
        if   s is Star.Type.Ia: return 12, AU(160), AU(3.1), AU(1.4), 6, d6(3)+3, -10
        elif s is Star.Type.Ib: return 10, AU(50), AU(1), AU(0.4), 6, d6(3)+2, -10
        elif s is Star.Type.II: return 6, AU(13), AU(0.3), AU(0.1), 6, d6(3)+1, -9
        elif s is Star.Type.III: return 2.7, AU(3.1), AU(0.1), 0, 6, d6(3), -8
        elif s is Star.Type.IV: return 1.8, AU(1), 0, 0, 7, d6(3)-1, -6
        elif s is Star.Type.V: return 1.1, AU(0.8), 0, 0, 16, d6(3)-2, 0
        else:                  return 0.8, AU(0.5), 0, 0, 16, d6(2)+1, 1
    elif t is Star.Class.K:
        if   s is Star.Type.Ia: return 15, AU(125), AU(2.5), AU(3), 10, d6(3)+2, -10
        elif s is Star.Type.Ib: return 12, AU(50), AU(1), AU(1), 16, d6(3)+2, -10
        elif s is Star.Type.II: return 6, AU(13), AU(0.3), AU(0.2), 16, d6(3)+1, -9
        elif s is Star.Type.III: return 3, AU(4), AU(0.1), 0, 16, d6(3), -7
        elif s is Star.Type.IV: return 2.3, AU(1), 0, 0, 16, d6(3)-1, -5
        elif s is Star.Type.V: return 0.9, (AU(0.5), AU(0.6)), 0, 0, 16, d6(3)-2, 0
        else:                  return 0.5, AU(0.2), 0, 0, 16, d6(2)+1, 1
    elif t is Star.Class.M:
        if   s is Star.Type.Ia: return 20, AU(100), AU(2), AU(7), 16, d6(3), -10
        elif s is Star.Type.Ib: return 16, AU(50), AU(1), AU(4.2), 16, d6(3), -10
        elif s is Star.Type.II: return 8, AU(16), AU(0.3), AU(1.1), 16, d6(3), -9
        elif s is Star.Type.III: return 4, AU(5), AU(0.1), AU(0.3), 16, d6(3), -6
        elif s is Star.Type.V: return 0.3, (AU(0.1), AU(0.2)), 0, 0, 16, d6(3)-2, 1
        else:                  return 0.2, (AU(0.1), AU(0.1)), 0, 0, 16, d6(2)+2, 2
    else:
        return 0.8, (AU(0.03), AU(0.03)), 0, 0, 0, 0, -10
