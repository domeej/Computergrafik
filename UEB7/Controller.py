from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
import sys, math

#import Oglviewer as ov
from Oglviewer import *



def mouse(button, state, x, y):

    global rotating, zooming, translating, mouseLastX, mouseLastY, startP, currentOrientation, angle, vpWidth, vpHeight

    if state == GLUT_UP:
        mouseLastX, mouseLastY = None, None

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            rotating = True

            r = min(vpWidth, vpHeight) / 2.0
            startP = projectOnSphere(x, y, r)
        if state == GLUT_UP:
            currentOrientation = currentOrientation * rotate(angle, axis)
            angle = 0
            rotating = False

    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            zooming = True
        if state == GLUT_UP:
            zooming = False

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            translating = True
        if state == GLUT_UP:
            translating = False

def mouseMoved(x, y):

    global mouseLastX, mouseLastY
    global angle, axis
    global zoomFactor
    global posX, posY

    xDiff = 0
    yDiff = 0

    # calc difference between act and last x,y mouse coordinates
    if mouseLastX:
        xDiff = x - mouseLastX
    if mouseLastY:
        yDiff = y - mouseLastY

    if rotating:
        r = min(vpWidth, vpHeight) / 2.0
        moveP = projectOnSphere(x, y, r)

        #abfangen falls beim rotieren 2x den gleichen Punkt -> Divisionsfehler
        if startP == moveP:
            return
        angle = math.acos(np.dot(startP, moveP))
        axis = np.cross(startP, moveP)
        glutPostRedisplay()

    if zooming:
        zScale = float(vpHeight) / 10
        if yDiff != 0:
            zoomFactor -= (yDiff / zScale)
            if zoomFactor < zoomMin:
                zoomFactor = zoomMin
            if zoomFactor > zoomMax:
                zoomFactor = zoomMax
            setProjection()

    if translating:
        scale = float(vpWidth) / 2.0
        if xDiff != 0:
            posX += xDiff / scale
        if yDiff != 0:
            posY += -yDiff / scale
        glutPostRedisplay()

    # Remember last x,y mouse coordinates
    mouseLastX = x
    mouseLastY = y


def keyPressed(key, x, y):

    global objColor, projectionMode, displayMode, shadow, animate
    global posX, posY
    global rotateX, rotateY, rotateZ
    global zoomFactor
    global angle, axis

    if key == '1':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*black)
        else:
            objColor = black
        glutPostRedisplay()

    if key == '2':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*white)
        else:
            objColor = white
        glutPostRedisplay()

    if key == '3':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*red)
        else:
            objColor = red
        glutPostRedisplay()

    if key == '4':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*green)
        else:
            objColor = green
        glutPostRedisplay()

    if key == '5':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*blue)
        else:
            objColor = blue
        glutPostRedisplay()

    if key == '6':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*yellow)
        else:
            objColor = yellow
        glutPostRedisplay()

    if key == 'p':
        if projectionMode == 'o':
            projectionMode = 'p'
            setProjection()
        elif projectionMode == 'p':
            projectionMode = 'o'
            setProjection()

    if key == 'd':
        if displayMode == 's':
            displayMode = 'w'
            glutPostRedisplay()
        elif displayMode == 'w':
            displayMode = 's'
            glutPostRedisplay()

    if key == 's':
        shadow = not shadow
        glutPostRedisplay()

    if key == 'r':
        posX, posY = 0.0, 0.0
        rotateX, rotateY, rotateZ = 0, 0, 0
        zoomFactor = 1.0
        angle, axis = 0, [0, 0, 1]
        setProjection()

    if key == 'a':
        animate = not animate