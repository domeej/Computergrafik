from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
from numpy import array
import sys, math



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
    if len(sys.argv) == 1:
        print ("keine Objektdatei angegeben!")
        sys.exit(-1)

    print("Datei " + sys.argv[1] + " wird verwendet!")

    # Punkte auslesen
    vertices, vertexnormals, faces = readOBJ(sys.argv[1])





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
    glBegin(GL_POLYGON)
    for i in range(6):
        glVertex2f(math.cos(i * math.pi / 3),\
                   math.sin(i * math.pi / 3))
    glEnd()
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
    # Start GLUT mainloop
    glutMainLoop()


if __name__ == "__main__":
    #main()
    initGeometryfromFile()

