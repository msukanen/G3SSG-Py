from .axialtilt import AxialTilt

class Planet:
    def __init__(self) -> None:
        self._density = None
        self._radius = None
        self._moons = None
        self._axtilt = AxialTilt()

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
