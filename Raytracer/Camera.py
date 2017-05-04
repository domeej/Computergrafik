import numpy as NP
import numpy.linalg as LA
from math import pi, tan

import Ray


class Camera(object):
    def __init__(self, position, target, up, fov, wres, hres):
        aspectratio = wres / hres  # Seitenverhaeltnis ausrechnen
        self.position = position  # position
        self.target = target  # center
        self.up = up
        self.aspectratio = aspectratio
        self.up = up
        self.fov = fov
        self.wres = wres
        self.hres = hres

        self.alpha = (fov/180. * pi) / 2
        self.height = 2 * tan(self.alpha)
        self.width = self.aspectratio * self.height

        self.f = (self.target - self.position).normalized()  # vector to center ('z-axis' vector)
        self.s = (self.f.cross(self.up)).normalized()  # 'x-axis' vector
        self.u = self.s.cross(self.f)  # 'y-axis' vector

    def calcray(self, x, y):
        """ Calculates a ray depending on its camera parameters and x and y pixels and . """
        pixelWidth = self.width / (self.wRes - 1)
        pixelHeight = self.height / (self.hRes - 1)
        #for y in range(self.hRes):
        #    for x in range(self.wRes):
        xcomp = self.s.scale(x * pixelWidth - self.width / 2)
        ycomp = self.u.scale(y * pixelHeight - self.height / 2)

        return  Ray(self.position, self.f + xcomp + ycomp)  # e v t l . mehrere S t r a h l e n pro P i x e l



    @classmethod
    def defaultcam(cls):
        origin = NP.array([0, 0, 0])
        target = NP.array([0, 3, 0])  #
        up = NP.array([0, 1, 0])
        fov = 45
        wres = 400
        hres = 400

        return Camera(origin, target, up, fov, wres, hres)
