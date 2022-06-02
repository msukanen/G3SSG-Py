import C
import K

def toC(a):
    if isinstance(a, C.C):
        return a
    if isinstance(a, K.K):
        return C.C(a.val - 273.15)
