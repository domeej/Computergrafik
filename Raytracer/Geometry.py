import math


class Entity(object):
    # hier moeglicherweise weiterer objektspezifischer code
    pass


class Sphere(Entity):
    """presentation of a sphere"""
    def __init__(self, center, radius, material):
        self.center = center  # point
        self.radius = radius  # scalar
        self.material = material

    def __repr__(self):
        return 'Sphere(%s, %s)' % (repr(self.center), self.radius)

    def intersectionParameter(self, ray): #VL
        co = self.center - ray.origin
        v = co.dot(ray.direction)
        discriminant = v * v - co.dot(co) + self.radius * self.radius
        if discriminant < 0:
            return None
        else:
            return v - math.sqrt(discriminant)

    def normalAt(self, p): #VL
        return (p - self.center).normalized()


class Plane(Entity):
    """presentation of a Plane"""
    def __init__(self, point, normal, material):
        self.point = point
        self.normal = normal.normalized()
        self.material = material

    def __repr__(self):
        return 'Plane(%s, %s)' % (repr(self.point), repr(self.normal))

    def intersectionParameter(self, ray): #VL
        op = ray.origin - self.point
        a = op.dot(self.normal)
        b = ray.direction.dot(self.normal)
        if b:
            return -a / b
        else:
            return None

    def normalAt(self, p): #VL
        return self.normal


class Triangle(Entity):
    """presentation of a Triangle"""
    def __init__(self, a, b, c, material):
        self.a = a  # point
        self.b = b  # point
        self.c = c  # point
        self.u = self.b - self.a  # directionvector
        self.v = self.c - self.a  # directionvector
        self.material = material

    def __repr__(self):
        return 'Triangle(%s, %s, %s)' % (repr(self.a), repr(self.b), repr(self.c))

    def intersectionParameter(self, ray): #VL
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

    def normalAt(self, p): #VL
        return self.u.cross(self.v).normalized()


class Ray(object):
    def __init__(self, origin, direction, level=1):
        self.origin = origin  # point
        self.direction = direction.normalized()  # vector
        self.level = level

    def __repr__(self):
        return 'Ray(%s, %s)' % (repr(self.origin), repr(self.direction))

    def pointAtParameter(self, t):
        return self.origin + self.direction.scale(t)


class Vector:
    """Vector with all it's Functions"""
    def __init__(self, p=None):
        if p == None:
            p = (0, 0, 0)
        self.x = p[0]
        self.y = p[1]
        self.z = p[2]

    def scale(self, scalar):
        v = (self.x * scalar, self.y * scalar, self.z * scalar)
        return Vector(v)

    def dot(self, other): #Skalarprodukt
        return (self.x * other.x + self.y * other.y + self.z * other.z)

    def norm(self): #Laenge
        return math.sqrt(self.dot(self))

    def normalized(self):
        return self.scale(1 / self.norm())

    def cross(self, other):
        newx = self.y * other.z - self.z * other.y
        newy = self.z * other.x - self.x * other.z
        newz = self.x * other.y - self.y * other.x
        return Vector((newx, newy, newz))

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))

    def __repr__(self):
        return 'Vector(%s, %s, %s)' % (repr(self.x), repr(self.y), repr(self.z))


class Material(object):
    def __init__(self, color):
        self.color = color
