import sys
sys.path.append(r'temperature')
from temperature import *

def hello():
    k = K(0)
    c = convert.toC(k)

    print(f'{k} = {c}')

if __name__=="__main__":
    sys.exit(hello())
