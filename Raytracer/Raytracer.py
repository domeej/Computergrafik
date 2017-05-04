import math
from PIL import Image

from Camera import Camera
import Light


class Ray(object):
    def __init__(self, origin, direction):
        self.origin = origin  # point
        self.direction = direction.normalized()  # vector

    def __repr__(self):
        return 'Ray(%s, %s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


class Sphere(object):
    def __init__(self, center, radius):
        self.center = center  # point
        self.radius = radius  # scalar

    def __repr__(self):
        return 'Sphere(%s, %s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray):
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v * v - co.dot(co) + self.radius * self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p):
        return (p - self.center).normalized()


class Plane(object):
    def __init__(self, point, normal):
        self.point = point
        self.normal = normal

    def __repr__(self):
        return 'Plane(%s, %s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray):
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a / b
        else:
            return None

    def normalAt(self, p):
        return self.normal


class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a  # point
        self.b = b  # point
        self.c = c  # point
        self.u = self.b - self.a  # directionvector
        self.v = self.c - self.a  # directionvector

    def __repr__(self):
        return 'Triangle(%s, %s, %s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray):
        w = ray.origin - self.a
        dv = ray.direction.cross(self.v)
        dvu = dv.dot(self.u)
        if dvu == 0.0:
            return None
        wu = w.cross(self.u)
        r = dv.dot(w) / dvu
        s = wu.dot(ray.direction) / dvu
        if 0 <= r and r <= 1 and 0 <= s and s <= 1 and r + s <= 1:
            return wu.dot(self.v) / dvu
        else:
            return None

    def normalAt(self, p):
        return self.u.cross(self.v).normalized()


class CheckerboardMaterial(object):
    def __init__(self, a, b, c):
        self.baseColor = (1, 1, 1)
        self.otherColor = (0, 0, 0)
        self.ambientCoefficient = 1.0
        self.diffuseCoefficient = 0.6
        self.specularCoefficient = 0.2
        self.checkSize = 1

    def baseColorAt(self, p):
        v = Vector(p)
        v.scale(1.0 / self.checkSize)
        if (int(abs(v.x) + 0.5) + int(abs(v.y) + 0.5) + int(abs(v.z) + 0.5)) % 2:
            return self.otherColor
            return self.baseColor


class Vector:
    def __init__(self, p=None):
        if p == None:
            p = (0, 0, 0)
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

    def scale(self, scalar):
        v = (self.x * scalar, self.y * scalar, self.z * scalar)
        return Vector(v)

    def dot(self, other):
        return (self.x * other.x + self.y * other.y + self.z * other.z)

    def norm(self):
        return math.sqrt(self.dot(self))

    def normalized(self):
        return self.scale(1 / self.norm())

    def cross(self, other):
        newx = self.y * other.z - self.z * other.y
        newy = self.z * other.x - self.x * other.z
        newz = self.x * other.y - self.y * other.x
        return Vector((newx, newy, newz))

    def __add__(self, other):
        return self.x + other.x, self.y + other.y, self.z + other.z

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y, self.z - other.z

    def __repr__(self):
        return 'Vector(%s, %s, %s)' % (repr(self.x), repr(self.y), repr(self.z))




def main():
    lightList = []
    lightList.append(Vector((30,30,10)))
    cam = Camera(Vector((0, 1.8, 10)), Vector((0, 3, 0)), Vector((0, 1, 0)), 45, 400, 400)


    objectlist = []
    plane = Plane(Vector((0, 0, 0)), Vector((0, 1, 0)))
    sphere1 = Sphere(Vector((-1.5, 3, 0)), 1)
    sphere2 = Sphere(Vector((1.5, 3, 0)), 1)
    sphere3 = Sphere(Vector((0, 5.5, 0)), 1)
    triangle = Triangle(Vector((-1.5, 3, 0)), Vector((1.5, 3, 0)), Vector((0, 5.5, 0)))
    objectlist.append(plane)
    objectlist.append(sphere1)
    objectlist.append(sphere2)
    objectlist.append(sphere3)
    objectlist.append(triangle)

    image = Image.new("RGB", (cam.wres, cam.hres))

    for x in range(cam.wres):
        for y in range(cam.hres):
            ray = cam.calcRay(x, y)
            maxdist = float('inf')
            color = (255,255,0)
            for object in objectlist:
                hitdist = object.intersectionParameter(ray)
                if hitdist and hitdist > 0:
                    if hitdist < maxdist:
                        maxdist = hitdist
                        color = (int(hitdist), int(hitdist), int(hitdist))
            image.putpixel((x, y), color)


    image.show()

    #######


if __name__ == '__main__':
    main()
