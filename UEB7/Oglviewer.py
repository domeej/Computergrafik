from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
import sys
import math
from Fileparser import readOBJ


DEFAULT_WIDTH, DEFAULT_HEIGHT = 500, 500

black = (0.0, 0.0, 0.0, 0.0)
white = (1.0, 1.0, 1.0, 0.0)
blue = (0.0, 0.0, 1.0, 0.0)
green = (0.0, 1.0, 0.0, 0.0)
yellow = (1.0, 1.0, 0.0, 0.0)
red = (1.0, 0.0, 0.0, 0.0)
startcolor = (0.2, 0.8, 0.4, 0.0)

the_vbo, data = None, None
boundingBox, center, heightOffset = None, None, 0

displayMode, projectionMode, = 's', 'p'
objColor = startcolor
shadowColor = (0.05, 0.05, 0.05, 0.0)

translating, rotating, zooming, animate, shadow = False, False, False, False, True
mouseLastX, mouseLastY = None, None
posX, posY = 0.0, 0.0
rotateX, rotateY, rotateZ = 0, 0, 0
zoomFactor, zoomMin, zoomMax = 1.0, 0.5, 10.0
angle, axis = 0, [0, 0, 1]
startP = None
currentOrientation = np.identity(4)

fov = 45.0
near = 0.1
far = 100.0
light = None


def initGL():
    """Startbedingungen festlegen"""
    global vpWidth, vpHeight
    vpWidth, vpHeight = DEFAULT_WIDTH, DEFAULT_HEIGHT

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glClearColor(*white)

    changeProjection()


def initGeometry():
    """liest die Faces aus, berechnet die Normalen falls keine in der Datei vorhanden waren und laedt die Daten in das VBO"""
    global the_vbo, data, boundingBox, center, scaleFactor, light
    objVertices, objNormals, objFaces = readOBJ(sys.argv[1])

    print("Lade Datei: " + sys.argv[1])

    # Setze die Groesse der Bounding Box auf die Groesse des models
    boundingBox = [map(min, zip(*objVertices)), map(max, zip(*objVertices))]
    scaleFactor = 2.0 / max([(x[1] - x[0]) for x in zip(*boundingBox)])
    center = [(x[0] + x[1]) / 2.0 for x in zip(*boundingBox)]
    # Licht abhaengig von der Groesse der Bounding-Box (evtl noch von Welt -> aktuelle Kamerakoordinaten)
    light = [boundingBox[1][0] * 2, boundingBox[1][1] * 3, boundingBox[1][2] / 2]

    data = generateData(objVertices, objNormals, objFaces)
    the_vbo = vbo.VBO(np.array(data, "f"))


def generateData(objVertices, objNormals, objFaces):
    """generiert die Daten fuer die VBO"""
    d = []

    for face in objFaces:

        if not objNormals:
            ncalc = calcNormal(objVertices, face)
        for vertex in face:
            vi = vertex[0]
            ni = vertex[2]

            if objNormals:
                d.append(objVertices[vi] + objNormals[ni])
            else:
                d.append(np.append(np.array(objVertices[vi]), ncalc))
    return d


def calcNormal(objVertices, face):
    """berechnet eine kuenstliche Normale"""
    C = objVertices[face[2][0]]
    B = objVertices[face[1][0]]
    A = objVertices[face[0][0]]

    normal = np.cross(np.subtract(B, A), np.subtract(C, A))
    return normal


def projectOnSphere(x, y, radius):
    """Arcball-Rotation"""
    x, y = x - vpWidth / 2.0, vpHeight / 2.0 - y
    a = min(radius * radius, x * x + y * y)
    z = math.sqrt(radius * radius - a)
    l = math.sqrt(x * x + y * y + z * z)
    return x / l, y / l, z / l


def rotate(angle, axis):
    """haendelt die Rotation"""
    c, mc = math.cos(angle), 1 - math.cos(angle)
    s = math.sin(angle)
    l = math.sqrt(np.dot(np.array(axis), np.array(axis)))
    x, y, z = np.array(axis) / l
    r = np.matrix(
        [[x * x * mc + c, x * y * mc - z * s, x * z * mc + y * s, 0],
         [x * y * mc + z * s, y * y * mc + c, y * z * mc - x * s, 0],
         [x * z * mc - y * s, y * z * mc + x * s, z * z * mc + c, 0],
         [0, 0, 0, 1]])
    return r.transpose()


def changeProjection():
    """berechnet die neue Matrix abhaengig der aktuellen Kamera-Position des Oeffnungswinkels usw.
    und beruecksichtigt die gewuenschten Projektion"""
    global fov, near, far
    aspectratio = float(vpWidth) / vpHeight

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # wechseln zwischen ortoghonal und perspektivischer Projektion
    if projectionMode == 'o':
        glOrtho(-1.0 * aspectratio / zoomFactor, 1.0 * aspectratio / zoomFactor, -1.0 / zoomFactor, 1.0 / zoomFactor, -10.0, 10.0)
    elif projectionMode == 'p':
        gluPerspective(fov / zoomFactor, aspectratio, near, far)

    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()


def resize(width, height):
    """Wird aufgerufen sobald das Window veraendert wird"""
    global vpWidth, vpHeight
    #verhindert division durch 0
    if height == 0:
        height = 1

    vpWidth, vpHeight = width, height

    glViewport(0, 0, int(width), int(height))
    changeProjection()


def animation():
    """drehe das Objekt um die y-Achse"""
    global rotateX, rotateY, rotateZ
    speed = 0.4
    if animate:
        rotateY = (rotateY + speed) % 360
        glutPostRedisplay()


def mouse(button, state, x, y):
    """Hier wird auf die unterschiedlichen Maus-Events reagiert"""
    global rotating, zooming, translating, mouseLastX, mouseLastY, startP, currentOrientation, angle

    if state == GLUT_UP:
        mouseLastX, mouseLastY = None, None

    #linke Taste gedrueckt
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            radius = min(vpWidth, vpHeight) / 2.0
            startP = projectOnSphere(x, y, radius)
            rotating = True
        if state == GLUT_UP:
            currentOrientation = currentOrientation * rotate(angle, axis)
            angle = 0
            rotating = False
    #mittlere Taste gedrueckt
    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            zooming = True
        if state == GLUT_UP:
            zooming = False
    #rechte Taste gedrueckt
    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            translating = True
        if state == GLUT_UP:
            translating = False


def mouseMoved(x, y):
    """Wird aufgerufen sobald eine Taste gedrueckt wurde und sich die Maus bewegt"""
    global mouseLastX, mouseLastY
    global angle, axis
    global zoomFactor
    global posX, posY
    global zoomMin, zoomMax
    xDiff = 0
    yDiff = 0

    # calc difference between act and last x,y mouse coordinates
    if mouseLastX:
        xDiff = x - mouseLastX
    if mouseLastY:
        yDiff = y - mouseLastY

    if translating:
        scale = float(vpWidth) / 2.0
        if xDiff != 0:
            posX += xDiff / scale
        if yDiff != 0:
            posY += -yDiff / scale
        glutPostRedisplay()

    if rotating:
        radius = min(vpWidth, vpHeight) / 2.0
        moveP = projectOnSphere(x, y, radius)
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
            changeProjection()

    # Merken der letzten x,y Koordinaten
    mouseLastX = x
    mouseLastY = y


def keyPressed(key, x, y):
    """faengt alle Keyevents ab"""
    global objColor, projectionMode, displayMode, shadow, animate
    global posX, posY
    global rotateX, rotateY, rotateZ
    global zoomFactor
    global angle, axis

    if key == 's':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*black)
        else:
            objColor = black
        glutPostRedisplay()

    if key == 'w':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*white)
        else:
            objColor = white
        glutPostRedisplay()

    if key == 'r':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*red)
        else:
            objColor = red
        glutPostRedisplay()

    if key == 'g':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*yellow)
        else:
            objColor = yellow
        glutPostRedisplay()

    if key == 'b':
        if glutGetModifiers() == GLUT_ACTIVE_ALT:
            glClearColor(*blue)
        else:
            objColor = blue
        glutPostRedisplay()

    if key == 'o':
        projectionMode = 'o'
        changeProjection()

    if key == 'p':
        projectionMode = 'p'
        changeProjection()

    if key == 'd':
        if displayMode == 's':
            displayMode = 'w'
            glutPostRedisplay()
        elif displayMode == 'w':
            displayMode = 's'
            glutPostRedisplay()

    if key == 'h':
        shadow = not shadow
        glutPostRedisplay()

    if key == 'n':
        # Ansicht zu Objektzentrum zuruecksetzen
        posX, posY = 0.0, 0.0
        rotateX, rotateY, rotateZ = 0, 0, 0
        zoomFactor = 1.0
        angle, axis = 0, [0, 0, 1]
        changeProjection()

    if key == 'a':
        animate = not animate



def display():
    """Wird fuer jedes Frame 1x aufgerufen, zeichnet die Szene"""
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # define a viewing transformation
    gluLookAt(-2, 0, 4, 0, 0, 0, 0, 1, 0)

    # Render Vertex Buffer Object
    the_vbo.bind()
    glVertexPointer(3, GL_FLOAT, 24, the_vbo)
    glNormalPointer(GL_FLOAT, 24, the_vbo + 12)

    glTranslate(posX, posY, 0.0)
    matrix = currentOrientation * rotate(angle, axis)
    glMultMatrixf(matrix.tolist())
    glRotate(rotateX, 1, 0, 0)
    glRotate(rotateY, 0, 1, 0)
    glRotate(rotateZ, 0, 0, 1)

    glScale(scaleFactor, scaleFactor, scaleFactor)
    glTranslate(-center[0], -center[1], -center[2])
    glColor(objColor)

    displayObjectbyMode()

    the_vbo.unbind()
    glutSwapBuffers()


def displayObjectbyMode():
    """Zeigt das Model abhaengig des displayMode's an"""
    # solid
    if displayMode == 's':
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)
        glCullFace(GL_BACK)
        glLight(GL_LIGHT0, GL_POSITION, light)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawArrays(GL_TRIANGLES, 0, len(data))
        # Schatten nur bei solid?
        if shadow:
            glPushMatrix()  # save state
            p = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0 / light[1], 0, 0, 1.0, 0, 0, 0, 0, 0]
            glTranslatef(light[0], light[1], light[2])  # translate back
            glTranslate(0.0, boundingBox[0][1], 0.0)
            glMultMatrixf(p)  # project object
            glTranslate(0.0, -boundingBox[0][1], 0.0)
            glTranslatef(-light[0], -light[1], -light[2])  # move light to origin
            glColor(*shadowColor)
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glDisable(GL_COLOR_MATERIAL)
            glDisable(GL_NORMALIZE)
            glDrawArrays(GL_TRIANGLES, 0, len(data))
            glPopMatrix()  # restore state

    # polygon-web
    elif displayMode == 'w':
        glDisable(GL_LIGHT0)
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_NORMALIZE)
        glDisable(GL_COLOR_MATERIAL)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawArrays(GL_TRIANGLES, 0, len(data))
        # schatten
        if shadow:
            glPushMatrix()  # save state
            p = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0 / light[1], 0, 0, 1.0, 0, 0, 0, 0, 0]
            glTranslatef(light[0], light[1], light[2])  # translate back
            glTranslate(0.0, boundingBox[0][1], 0.0)
            glMultMatrixf(p)  # project object
            glTranslate(0.0, -boundingBox[0][1], 0.0)
            glTranslatef(-light[0], -light[1], -light[2])  # move light to origin
            glColor(*shadowColor)
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glDisable(GL_COLOR_MATERIAL)
            glDisable(GL_NORMALIZE)
            glDrawArrays(GL_TRIANGLES, 0, len(data))
            glPopMatrix()  # restore state


def main():
    if len(sys.argv) != 2:
        print "keine Datei gefunden"
        sys.exit(-1)
    else:
        print "Datei: "+ sys.argv[1]

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    glutCreateWindow("Verrueckter OGLViewer")

    glutDisplayFunc(display)
    glutReshapeFunc(resize)
    glutKeyboardFunc(keyPressed)
    glutMouseFunc(mouse)
    glutMotionFunc(mouseMoved)
    glutIdleFunc(animation)

    initGeometry()
    initGL()

    glutMainLoop()


if __name__ == '__main__':
    main()
