import numpy as NP

import Camera
import Light
from Geometry import Triangle, Plane, Sphere, Material


class Scene(object):
    def __init__(self):
        self.objects = []

        self.light = Light()
        self.camera = Camera.defaultcam()

        self.objects.append(Plane(NP.aray([0, 1, 0]), Plane(NP.aray([0, 0, 0]), Material())))
        self.objects.append(Sphere(5, NP.aray([-3, 0, 0]), Material()))
        self.objects.append(Sphere(5, NP.aray([3, 0, 0]), Material()))
        self.objects.append(Sphere(5, NP.aray([0, 6, 0]), Material()))
        self.objects.append(
            Triangle(NP.aray([-3, 0, 0]), NP.aray([3, 0, 0], NP.aray([0, 6, 0]), NP.aray([0, 0, 0]), material())))

    def renderImage(self):
        s = NP.cross(Camera.direction, Camera.)
