import numpy.linalg as LA
import numpy as NP

class Ray (object):

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalized()
        #self.direction = direction / LA.norm(direction) #Vektor / Laenge = normalisierter Vektor


    def pointAtParameter(self, t):
        return self.origin + self.direction *t


if __name__ == "__main__":


    #x = Ray(NP.array([1,1,1], NP.array([2,3,0])))
    a = NP.array([2,3,2])
    a = LA.norm(a) #laenge
    print(a)
    b = 4
    print(b.scale(2))


