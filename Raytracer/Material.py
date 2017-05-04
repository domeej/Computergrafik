from Geometry import Vector


class Material(object):
    def __init__(self, amb, dif, spec, color, ref=0):
        self.amb = amb
        self.dif = dif
        self.spec = spec
        self.ref = ref
        self.color = color

    def baseColorAt(self, p):
        return self.color


class CheckerboardMaterial(object):
    def __init__(self, amb, dif, spec, ref=0):
        self.baseColor = Vector((255, 255, 255))
        self.otherColor = Vector((0, 0, 0))
        self.amb = amb
        self.dif = dif
        self.spec = spec
        self.checkSize = 1
        self.ref = ref

    def baseColorAt(self, p):
        p.scale(1.0 / self.checkSize)
        if (int(abs(p.x) + 0.5) + int(abs(p.y) + 0.5) + int(abs(p.z) + 0.5)) % 2:
            return self.otherColor
        return self.baseColor