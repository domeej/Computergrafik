from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array
import sys, math

data = []
my_vbo = None

def readOBJ(filename):

    vertices = []
    vertexnormals = []
    faces = []

    for line in open(filename):
        if line.split():
            line = line.split()

            if line[0] == 'v':
                vertices.append(map(float, line[1:]))
            if line[0] == 'vn':
                vertexnormals.append(float(line[1:]))
            if line[0] == 'f':
                faces.append(map(int, line[1:]))

    return (vertices, vertexnormals, faces)

def initGeometryfromFile():
    global my_vbo, data

    if len(sys.argv) == 1:
        print ("keine Objektdatei angegeben!")
        sys.exit(-1)

    print("Datei " + sys.argv[1] + " wird verwendet!")

    # Punkte auslesen
    vertices, vertexnormals, faces = readOBJ(sys.argv[1])

    data = []

    # Create BoundingBox
    boundingBox = [map(min, zip(*vertices)), map(max, zip(*vertices))]
    # Calc center of bounding box
    center = [(x[0] + x[1]) / 2.0 for x in zip(*boundingBox)]
    # Calc scale factor
    scaleFactor = 2.0 / max([(x[1] - x[0]) for x in zip(*boundingBox)])

    # get the right data for the vbo
    for vertex in faces:
        vn = int(vertex[0]) - 1
        nn = int(vertex[2]) - 1
        if vertexnormals:
            data.append(vertices[vn] + vertexnormals[nn])
        else:
            # calc standard normals, if no objectNormals available
            normals = [x - y for x, y in zip(vertices[vn], center)]
            l = math.sqrt(normals[0] ** 2 + normals[1] ** 2 + normals[2] ** 2)
            normals = [x / l for x in normals]
            data.append(vertices[vn] + normals)

    my_vbo = vbo.VBO(array(data, 'f'))





def initGL(width, height):
    # Set background color to blue
    glClearColor(0.0, 0.0, 1.0, 0.0)
    # Set orthograpicprojection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-1.5, 1.5, -1.5, 1.5, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)


def display():

    # Clear frame buffer
    glClear(GL_COLOR_BUFFER_BIT)
    # Set color to light gray
    glColor3f(.75, .75, .75)
    # Set draws tyle
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    # Set primitive type to polygon

    vbo.bind()

    glVertexPointerf(vbo)
    glEnableClientState(GL_VERTEX_ARRAY)
    glDrawArrays(GL_POLYGON, 0, len(data))

    vbo.unbind()


    glDisableClientState(GL_VERTEX_ARRAY)


    # Flush commands
    glFlush()


def main():
    # Initialize GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow("Einfaches OpenGL Programm")
    # Registerdisplaycallbackfunction
    glutDisplayFunc(display)
    # Initialize OpenGL context
    initGL(500, 500)

    initGeometryfromFile()

    # Start GLUT mainloop
    glutMainLoop()


if __name__ == "__main__":
    main()


