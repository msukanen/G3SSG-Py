from .star import Star
from .axialtilt import AxialTilt
from distance import mi
from dice import d6
from .moons import Moon
from .density import Density

__EARTH_RAD = mi(7915) / 2
__EARTH_DNS = 5.5

class Planet:
    def __init__(self, star:Star, oid:int) -> None:
        self.__density = None
        self.__radius = None
        self._moons = None
        self._axtilt = AxialTilt()
        self.__lod = None
        self.__orbit_index = oid

    @property
    def density(self) -> float:
        """Get planet's density."""
        return self.__density
    @density.setter
    def density(self, d:Density) -> Density:
        """Set planet's density. Do nothing if already set..."""
        if self.__density == None:
            self.__density = d
        return self.__density

    @property
    def gravity(self) -> float:
        """Figure out the local gravity."""
        return (self._radius/__EARTH_RAD) * (self._density/__EARTH_DNS)

    @property
    def radius(self) -> float:
        """Get radius (in one or other suitable unit)."""
        return self.__radius
    @radius.setter
    def radius(self, r:float) -> float:
        """Set radius, if not already set."""
        if self.__radius != None:
            self.__radius = r
        return self.__radius

    @property
    def moons(self) -> dict:
        """Get the moon(s)!"""
        return self._moons

    @property
    def axial_tilt(self) -> AxialTilt:
        """Get axial tilt."""
        return self._axtilt

    @property
    def day_length(self) -> int:
        """Get length of day (in hours); None if planet is tide locked."""
        return self.__lod

    def _determine_day_length(self) -> int:
        """Determine day length..."""
        mod = 0
        if self.__orbit_index == 1:
            mod -= 4
        elif self.__orbit_index == 2:
            mod -= 2
        if (Moon.Type.Giant in self._moons) or (Moon.Type.SmallGG in self._moons):
            mod -= 1
        if self._radius < 0.5*__EARTH_RAD:
            mod -= 1
        elif self._radius > 9*__EARTH_RAD:
            mod += 3
        elif self._radius > 6*__EARTH_RAD:
            mod += 2
        elif self._radius > 3*__EARTH_RAD:
            mod += 1
        r = d6(2)+mod
        if r <= 2:
            self.__lod = d6(2)*10*24
        else:
            match r:
                case 3: self.__lod = d6()*12*24
                case 4: self.__lod = d6()*5*24
                case 5: self.__lod = d6(2)*10
                case 6: self.__lod = d6()*10
                case _: self.__lod = d6(14-max(3,r))
