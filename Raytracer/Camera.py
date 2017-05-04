import numpy as NP
from math import pi, tan
from Geometry import Ray

class Camera(object):
    def __init__(self, position, target, up, fov, wres, hres):
        aspectratio = float(wres) / hres  # Seitenverhaeltnis ausrechnen
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

    def __repr__(self):
        return 'Camera(pos: %s, dir: %s, up: %s, fov: %s, wres: %s, hres: %s)' % (
        repr(self.position), repr(self.f), repr(self.up), repr(self.fov), repr(self.wres), repr(self.hres))

    def calcRay(self, x, y):
            """ Calculates a ray depending on its camera parameters and x and y pixels. """
            y = self.hres - y
            pixelWidth = self.width / (self.wres - 1)
            pixelHeight = self.height / (self.hres - 1)
            xcomp = self.s.scale(x * pixelWidth - self.width / 2)
            ycomp = self.u.scale(y * pixelHeight - self.height / 2)
            ray = Ray(self.position, self.f + xcomp + ycomp)  # e v t l . mehrere S t r a h l e n pro P i x e l
            return ray

    @classmethod
    def defaultcam(cls):
        origin = NP.array([0, 0, 0])
        target = NP.array([0, 3, 0])  #
        up = NP.array([0, 1, 0])
        fov = 45
        wres = 400
        hres = 400

        return Camera(origin, target, up, fov, wres, hres)
