import sys
from starsystem.star import Star
from temperature import *
from distance import *
from dice import *
from starsystem import *

def hello():
    s = Star()
    print(s)
    for x in range(s.numOrbits):
        pass#print(f"orbit {x}")

if __name__=="__main__":
    sys.exit(hello())
