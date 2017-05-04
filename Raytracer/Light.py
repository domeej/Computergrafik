import numpy as NP

class Light(object):

    def __init__(self, position):
        #color FEHLT NOCH
        self.position = position

    @classmethod
    def defaultLight(cls):
        position = NP.array([30, 30, 10])
        return Light(position)


