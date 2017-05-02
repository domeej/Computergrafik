class Entity(object):
    #hier noch objektspezifischer code
    pass

class Sphere(Entity):
    # translation Verschiebungsvektor
    def __init__(self, center, radius, translation, material):
        self.center = center
        self.radius = radius
        self.translation = translation
        self.material = material


class Plane(Entity):
    def __init__(self, point, normal, translation, material):
        # normal gibt an wie die ebene auf dem punkt liegt
        self.point = point
        self.normal = normal
        self.translation = translation
        self.material = material


class Triangle(Entity):
    def __init__(self, a, b, c, translation, material):
        self.a = a
        self.b = b
        self.c = c
        self.translation = translation
        self.material = material
        self.u = self.b - self.a #direction vector
        self.v = self.c - self.a #direction vector


class Material(object):
    def __init__(self, color):
        self.color = color

