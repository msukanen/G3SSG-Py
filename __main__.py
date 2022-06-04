import sys
from starsystem.star import Star
from temperature import *
from distance import *
from dice import *
from starsystem import *

def hello():
    k = K(0)
    c = toC(k) * 2

    print(f'{k} = {c}')

    a = AU(1)
    l = toLY(a)
    p = pc(l*6 + 3)
    print(f'{a} = {l}')
    print(f'{p}')

    r = d6(2)
    print(f'r = {r}')

    s = Star()
    print(f'{s}')

if __name__=="__main__":
    sys.exit(hello())
