from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array, subtract, cross, append
import sys

# global data
DEFAULT_WIDTH, DEFAULT_HEIGHT = 500, 500

black = (0.0,0.0,0.0,0.0)
white = (1.0,1.0,1.0,0.0)
blue = (0.0,0.0,1.0,0.0)
green = (0.0,1.0,0.0,0.0)
yellow = (1.0,1.0,0.0,0.0)
red = (1.0,0.0,0.0,0.0)

my_vbo, data = None, None
boundingBox, center, heightOffset = None, None, 0

fov = 45.0
near = 0.1
far = 100.0

translating, rotating, zooming, animate = False, False, False, False
mouseLastX, mouseLastY = None, None
posX, posY = 0.0, 0.0
rotateX, rotateY, rotateZ = 0, 90, 0
zoomFactor, zoomMin, zoomMax = 1.0, 0.5, 10.0

displayMode, projectionMode, shadow = 's', 'p', True
light = [500.0, 2000.0, 1.0]

def loadOBJ(filename):
    vertices = []
    normals = []
    faces = []

    print "Loading File: ", sys.argv[1] + "..."

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("v "):
                vertices.append(map(float,line.split()[1:]))
            elif line.startswith("vn "):
                normals.append(map(float, line.split()[1:]))
            elif line.startswith("f "):
                face = []
                for vertex_as_string in line.split()[1:]:
                    vertex_as_string_list = vertex_as_string.split("/")
                    v = int(vertex_as_string_list[0])-1
                    t = -1
                    n = -1
                    if len(vertex_as_string_list) > 1 and vertex_as_string_list[1]:
                        t = int(vertex_as_string_list[1])-1
                    if len(vertex_as_string_list) > 2 and vertex_as_string_list[2]:
                        n = int(vertex_as_string_list[2])-1
                    face.append([v, t, n])
                faces.append(face)
    return (vertices, normals, faces)

def initGL():

    global vpWidth, vpHeight
    vpWidth, vpHeight = DEFAULT_WIDTH, DEFAULT_HEIGHT

    glClearColor(*white)
    setProjection()

def initGeometry():

    global my_vbo, data, boundingBox, center, scaleFactor, heightOffset

    vertices, normals, faces = loadOBJ(sys.argv[1])
    data = []

    boundingBox = [map(min, zip(*vertices)), map(max, zip(*vertices))]
    center = [(x[0] + x[1]) / 2.0 for x in zip(*boundingBox)]
    scaleFactor = 2.0 / max([(x[1] - x[0]) for x in zip(*boundingBox)])
    heightOffset = (boundingBox[1][1]-boundingBox[0][1])/2*scaleFactor

    for face in faces:
        if not normals:
            A, B, C = vertices[face[0][0]], vertices[face[1][0]], vertices[face[2][0]]
            ncalc = cross(subtract(B, A), subtract(C, A))
        for vertex in face:
            vi = vertex[0]
            ni = vertex[2]

            if normals:
                data.append(vertices[vi] + normals[ni])
            else:
                data.append(append(array(vertices[vi]), ncalc))

    my_vbo = vbo.VBO(array(data, "f"))

def setProjection():

    global vpWidth, vpHeight, zoomFactor

    aspect = float(vpWidth) / vpHeight

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if projectionMode == 'o':
        glOrtho(-1.0 * aspect / zoomFactor, 1.0 * aspect / zoomFactor, (-1.0+heightOffset) / zoomFactor, (1.0+heightOffset) / zoomFactor, -10.0, 10.0)
    elif projectionMode == 'p':
        gluPerspective(fov / zoomFactor, aspect, near, far)
        gluLookAt(0, heightOffset, 3, 0, heightOffset, 0, 0, 1, 0)

    glMatrixMode(GL_MODELVIEW)
    glutPostRedisplay()

def mouse(button, state, x, y):

    global translating, zooming, mouseLastX, mouseLastY

    if state == GLUT_UP:
        mouseLastX, mouseLastY = None, None

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            translating = True
        if state == GLUT_UP:
            translating = False

    if button == GLUT_MIDDLE_BUTTON:
        if state == GLUT_DOWN:
            zooming = True
        if state == GLUT_UP:
            zooming = False

def mouseMoved(x, y):

    global vpWidth, vpHeight
    global mouseLastX, mouseLastY
    global translating, zooming
    global zoomFactor, zoomMin, zoomMax
    global posX, posY

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

    if zooming:
        zScale = float(vpHeight) / 10
        if yDiff != 0:
            zoomFactor -= (yDiff / zScale)
            if zoomFactor < zoomMin:
                zoomFactor = zoomMin
            if zoomFactor > zoomMax:
                zoomFactor = zoomMax
            setProjection()


    # Remember last x,y mouse coordinates
    mouseLastX = x
    mouseLastY = y


def keyPressed(key, x, y):

    global projectionMode, displayMode, animate

    if key == 'o':
        if projectionMode == 'p':
            projectionMode = 'o'
            setProjection()
    if key == 'p':
        if projectionMode == 'o':
            projectionMode = 'p'
            setProjection()

    if key == 'w':
        if displayMode == 's':
            displayMode = 'w'
            glutPostRedisplay()
    if key == 's':
        if displayMode == 'w':
            displayMode = 's'
            glutPostRedisplay()

    if key == 'a':
        animate = not animate

def resize(width, height):

    if height == 0:
        height = 1

    global vpWidth, vpHeight
    vpWidth, vpHeight = width, height

    glViewport(0, 0, int(width), int(height))
    setProjection()

def display():

    global my_vbo, data
    global displayMode, shadow, light
    global scaleFactor, center, heightOffset, rotateX, rotateY, rotateZ, posX, posY

    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    my_vbo.bind()
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glVertexPointer(3, GL_FLOAT, 24, my_vbo)
    glNormalPointer(GL_FLOAT, 24, my_vbo + 12)

    glTranslate(0, heightOffset, 0)

    glTranslate(posX, posY, 0.0)
    glRotate(rotateX, 1, 0, 0)
    glRotate(rotateY, 0, 1, 0)
    glRotate(rotateZ, 0, 0, 1)

    glScale(scaleFactor, scaleFactor, scaleFactor)
    glTranslate(-center[0], -center[1], -center[2])

    if displayMode == 'w':
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_NORMALIZE)
        glColor(*blue)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDrawArrays(GL_TRIANGLES, 0, len(data))
    elif displayMode == 's':
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glColor(*blue)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDrawArrays(GL_TRIANGLES, 0, len(data))

        if shadow:
            glPushMatrix()  # save state
            p = [1.0, 0, 0, 0, 0, 1.0, 0, -1.0 / light[1], 0, 0, 1.0, 0, 0, 0, 0, 0]
            glTranslatef(light[0], light[1], light[2])  # translate back
            glMultMatrixf(p)  # project object
            glTranslatef(-light[0], -light[1], -light[2])  # move light to origin
            glColor(*black)
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glDisable(GL_COLOR_MATERIAL)
            glDisable(GL_NORMALIZE)
            glDrawArrays(GL_TRIANGLES, 0, len(data))
            glPopMatrix()  # restore state

    my_vbo.unbind()
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)

    glutSwapBuffers()

def animation():
    speed = 0.5
    global rotateX, rotateY, rotateZ
    if animate:
        rotateX = (rotateX + speed) % 360
        rotateY = (rotateY + speed) % 360
        rotateZ = (rotateZ + speed) % 360
        glutPostRedisplay()

def main():
    if len(sys.argv) != 2:
        print "python oglViewer.py objectFile.obj"
        sys.exit(-1)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(DEFAULT_WIDTH, DEFAULT_HEIGHT)
    glutCreateWindow("OpenGL ModelViewer")

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
