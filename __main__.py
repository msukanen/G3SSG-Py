import sys
from temperature import *
from distance import *

def hello():
    k = K(0)
    c = toC(k)

    print(f'{k} = {c}')

    a = AU(1)
    l = toLY(a)
    p = pc(l*6 + 3)
    print(f'{a} = {l}')

if __name__=="__main__":
    sys.exit(hello())
