def dictInc(d:dict, what, by:int = 1) -> None:
    if what in d:
        d[what] += by
    else: d[what] = (-1) + by
