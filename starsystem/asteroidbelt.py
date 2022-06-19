from dice import d6

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
