from dice import d6
from numbers import Number
from enum import Enum

class AxialTilt:
    class SeasonalEffect(Enum):
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
        elif isinstance(fixed, Number):
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

    @property
    def angle(self):
        return self.__tilt

    @property
    def seasonal_effect(self):
        return self.__seasonalEffect
