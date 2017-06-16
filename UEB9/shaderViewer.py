from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from glew import *
 
import sys, time

# choose a fragment-/vertex-shader 
#fragProg = open("simpleColor_fragment_shader.dat","r").read()
#vertProg = open("simpleColor_vertex_shader.dat","r").read()
#fragProg = open("toon_fragment_shader.dat","r").read()
#vertProg = open("toon_vertex_shader.dat","r").read()
fragProg = open("flag_fragment_shader.dat","r").read()
vertProg = open("flag_vertex_shader.dat","r").read()

# animation data
anglex, angley = 0, 0
animation = 0
t = 0


def idle():
    global anglex, angley, animation, t
    if animation:
        anglex = (anglex+1)%360
        angley = (angley+1)%360
        if anglex==0:
            animation, t = 0, 0
        sendValue("timeStep", t-int(t))
        t = time.clock()
        glutPostRedisplay()
    
    
def keyboard(key, x, y):
    global animation
    if key==chr(27): # chr(27) == EsCAPE
        sys.exit()
    if key=='a' or key=='a':
        animation = (animation+1)%2
    glutPostRedisplay()
    


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotate(anglex, 1,0,0)
    glRotate(angley, 0,1,0)
    glutSolidTeapot(0.5)
    glutSwapBuffers()


def initGL(width, height):
    global shaderHandle
    # creating a rendering context
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow("GLSL example")  
    
    # add callback functions
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    
    # checking if glew is available
    glewError = glewInit()
    if  glewError != GLEW_OK:
        print "glewInit return error: ", glewGetErrorString(1) 
    else:
        print "using GLEW version: ", glewGetString(GLEW_VERSION)
        
        # checking wether system supports ARB_(fragment,vertex)_programm extension
        fsSupport, vsSupport = True, True
        if not GLEW_ARB_fragment_program:
            print "system does not support the ARB_fragment_program extension"
            fsSupport = False
        if not GLEW_ARB_vertex_program:
            print "system does not support the ARB_vertex_program extension"
            vsSupport = False
    
        if fsSupport or vsSupport:
            # load shader
            if vsSupport:
                vsHandle = initShader(GL_VERTEX_SHADER_ARB, vertProg)
            if fsSupport:   
                fsHandle = initShader(GL_FRAGMENT_SHADER_ARB, fragProg)
            # link shader
            shaderHandle = linkShaders(vsHandle, fsHandle)
            # use GLSL shader
            if shaderHandle:
                glUseProgramObjectARB(shaderHandle)
            else:
                glUseProgramObjectARB(0)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [4.0, 3.0, -2.0 ,1.0])
    

def initShader(type, program):
    # create (fragment/vertex) shader program name (handle)
    shaderHandle = glCreateShaderObjectARB(type)
    # generate shader source
    glShaderSourceARB(shaderHandle, 1, [program])
    # compile shader
    glCompileShaderARB(shaderHandle)
    success = glGetObjectParameterivARB(shaderHandle, GL_OBJECT_COMPILE_STATUS_ARB)
    if not success: 
        print glGetInfoLogARB(program)
    return shaderHandle
    

def linkShaders(vsHandle, fsHandle):
    if vsHandle or fsHandle:  # generate shader program handle
        shaderHandle  = glCreateProgramObjectARB()
    if vsHandle: # attach vertex shader
        glAttachObjectARB(shaderHandle, vsHandle)
        glDeleteObjectARB(vsHandle)
    if fsHandle: # attach fragment shader
        glAttachObjectARB(shaderHandle, fsHandle)
        glDeleteObjectARB(fsHandle)
    # link shader program
    glLinkProgramARB(shaderHandle)
    # print link status
    success = glGetObjectParameterivARB(shaderHandle, GL_OBJECT_LINK_STATUS_ARB)
    if not success:
        print glGetInfoLogARB(handle)
    return shaderHandle
    
def sendValue(varName, value):
    # determine location of uniform variable timeElapsed
    var = glGetUniformLocationARB(shaderHandle, varName)
    # pass value to shader
    glUniform1fARB(var, value)
    

if __name__ == "__main__":
    initGL(400, 400)
    glutMainLoop()
    