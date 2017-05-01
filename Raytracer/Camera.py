import numpy as NP
import numpy.linalg as LA
import math


class Camera(object):
    def __init__(self, origin, target, up, fov, aspectratio, wres, hres):
        self.origin = origin
        direction = target - origin
        direction /= LA.norm(direction)
        self.direction = direction
        self.aspectratio = aspectratio
        self.fov = fov
        self.wres = wres
        self.hres = hres




    @classmethod
    def defaultcam(cls):

        origin = NP.array([0, 0, 0])
        target = NP.array([0, 3, 0])#
        # up =
        fov = 45
        wres = 400
        hres = 400
        aspectratio = wres / hres
        up = NP.array([0,1,0])
        return Camera(origin, direction, up, fov, aspectratio, wres, hres)
