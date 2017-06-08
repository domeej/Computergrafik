import numpy as np


class Variables:
    def __init__(self):
        self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT = 500, 500
        self.black = (0.0, 0.0, 0.0, 0.0)
        self.white = (1.0, 1.0, 1.0, 0.0)
        self.blue = (0.0, 0.0, 1.0, 0.0)
        self.green = (0.0, 1.0, 0.0, 0.0)
        self.yellow = (1.0, 1.0, 0.0, 0.0)
        self.red = (1.0, 0.0, 0.0, 0.0)

        self.fov = 45.0
        self.near = 0.1
        self.far = 100.0
        self.light = None

        self.my_vbo, self.data = None, None
        self.boundingBox, self.center, self.heightOffset = None, None, 0

        self.displayMode, self.projectionMode, = 's', 'p'
        self.objColor = self.blue
        self.shadowColor = (0.1, 0.1, 0.1, 0.0)

        self.vpWidth = None
        self.vpHeight = None

        self.translating, self.rotating, self.zooming, self.animate, self.shadow = False, False, False, False, True
        self.mouseLastX, self.mouseLastY = None, None
        self.posX, self.posY = 0.0, 0.0
        self.rotateX, self.rotateY, self.rotateZ = 0, 0, 0
        self.zoomFactor, self.zoomMin, self.zoomMax = 1.0, 0.5, 10.0
        self.angle, self.axis = 0, [0, 0, 1]
        self.startP = None
        self.currentOrientation = np.identity(4)

    @property
    def DEFAULT_WIDTH(self):
        return self.DEFAULT_WIDTH

    @DEFAULT_WIDTH.setter
    def DEFAULT_WIDTH(self, value):
        self.DEFAULT_WIDTH = value

    @property
    def DEFAULT_HEIGHT(self):
        return self.DEFAULT_HEIGHT

    @DEFAULT_HEIGHT.setter
    def DEFAULT_HEIGHT(self, value):
        self.DEFAULT_HEIGHT = value

    @property
    def black(self):
        return self.black

    @property
    def white(self):
        return self.white

    @property
    def blue(self):
        return self.blue

    @property
    def green(self):
        return self.green

    @property
    def yellow(self):
        return self.yellow

    @property
    def red(self):
        return self.red

    @property
    def fov(self):
        return self.fov

    @property
    def far(self):
        return self.far

    @property
    def light(self):
        return self.light

    @property
    def my_vbo(self):
        return self.my_vbo

    @property
    def data(self):
        return self.data

    @property
    def boundingBox(self):
        return self.boundingBox

    @property
    def center(self):
        return self.center

    @property
    def heightOffset(self):
        return self.heightOffset

    @property
    def displayMode(self):
        return self.displayMode

    @property
    def projectionMode(self):
        return self.projectionMode

    @property
    def objColor(self):
        return self.objColor

    @property
    def shadowColor(self):
        return self.shadowColor

    @property
    def vpWidth(self):
        return self.vpWidth

    @property
    def vpHeight(self):
        return self.vpHeight

    @property
    def translating(self):
        return self.translating

    @property
    def rotating(self):
        return self.rotating

    @property
    def zooming(self):
        return self.zooming

    @property
    def animate(self):
        return self.animate

    @property
    def shadow(self):
        return self.shadow

    @property
    def mouseLastX(self):
        return self.mouseLastX

    @property
    def mouseLastY(self):
        return self.mouseLastY

    @property
    def posX(self):
        return self.posX

    @property
    def posY(self):
        return self.posY

    @property
    def rotateX(self):
        return self.rotateX

    @property
    def rotateY(self):
        return self.rotateY

    @property
    def rotateZ(self):
        return self.rotateZ

    @property
    def zoomFactor(self):
        return self.zoomFactor

    @property
    def zoomMin(self):
        return self.zoomMin

    @property
    def zoomMax(self):
        return self.zoomMax

    @property
    def angle(self):
        return self.angle

    @property
    def axis(self):
        return self.axis

    @property
    def startP(self):
        return self.startP

    @property
    def currentOrientation(self):
        return self.currentOrientation
