import numpy as NP
import numpy.linalg as LA
from math import pi, tan


class Camera(object):
    def __init__(self, origin, target, up, fov, wres, hres):
        direction = target - origin
        direction /= LA.norm(direction)  # normalisieren -> direction hat länge 1
        aspectratio = wres / hres  # Seitenverhaeltnis ausrechnen

        self.direction = direction
        self.aspectratio = aspectratio
        self.origin = origin
        self.up = up
        self.fov = fov
        self.wres = wres
        self.hres = hres

        self.alpha = (fov/180. * pi) / 2
        self.height = 2 * tan(self.alpha)
        self.width = self.aspectratio * self.height


    @classmethod
    def defaultcam(cls):
        origin = NP.array([0, 0, 0])
        target = NP.array([0, 3, 0])  #
        up = NP.array([0, 1, 0])
        fov = 45
        wres = 400
        hres = 400

        return Camera(origin, target, up, fov, wres, hres)
