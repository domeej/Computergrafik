from Tkinter import *
from Canvas import *
import sys
import random

WIDTH  = 400 # width of canvas
HEIGHT = 400 # height of canvas

HPSIZE = 1 # double of point size (must be integer)
COLOR = "#0000FF" # blue

NOPOINTS = 1000

pointList = [] # list of points (used by Canvas.delete(...))

def quit(root=None):
    """ quit programm """
    if root==None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()

def draw():
    """ draw points """
    for i in range(1,NOPOINTS):
	x, y = random.randint(1,WIDTH), random.randint(1,HEIGHT)
	p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                           fill=COLOR, outline=COLOR)
	pointList.insert(0,p)

def rotYp():
    """ rotate counterclockwise around y axis """
    global NOPOINTS
    NOPOINTS += 100
    print "In rotYp: ", NOPOINTS 
    can.delete(*pointList)
    draw()

def rotYn():
    """ rotate clockwise around y axis """
    global NOPOINTS
    NOPOINTS -= 100
    print "In rotYn: ", NOPOINTS 
    can.delete(*pointList)
    draw()


if __name__ == "__main__":
    #check parameters
    if len(sys.argv) != 1:
       print "pointViewerTemplate.py"
       sys.exit(-1)

    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
    
