from .axialtilt import AxialTilt
from distance import mi

__EARTH_RAD = mi(7915) / 2
__EARTH_DNS = 5.5

class Planet:
    def __init__(self) -> None:
        self._density = None
        self._radius = None
        self._moons = None
        self._axtilt = AxialTilt()
        self._lod = None

    @property
    def density(self) -> float:
        """Get planet's density."""
        return self._density

    @property
    def gravity(self) -> float:
        """Figure out the local gravity."""
        return (self._radius/__EARTH_RAD) * (self._density/__EARTH_DNS)

    @property
    def radius(self) -> float:
        """Get radius (in one or other suitable unit)."""
        return self._radius

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
        return self._lod

    def _determine_day_length(self) -> int:
        """Determine day length..."""
        