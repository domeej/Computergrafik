import numpy.linalg as LA
import numpy as NP

class Ray (object):

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction / LA.norm(direction) #Vektor / Laenge = normalisierter Vektor

if __name__ == "__main__":

    a = NP.array([2,3,2])
    a = LA.norm(a) #länge
    print(a)



