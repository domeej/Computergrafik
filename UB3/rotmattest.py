import sys
import numpy as np


if __name__ == "__main__":
     if len(sys.argv)<2:
	print "usage: rotmattest.py mat.dat"
	sys.exit(-1)
     filename = sys.argv[1]

     # read mat file and make numpy matrix
     mat = np.array([map(float,line.split()) for line in open(filename)])

     # determine det
     detMat = np.linalg.det(mat)
   
     # check wether det equals 1 or not 
     if not np.isclose(detMat,1):
	 print "Not a rotation matrix (det != 1)"
	 sys.exit(0)
     
     # check wether mat*mat^T = I
     I = np.dot(mat, mat.T)
     if not np.allclose(I, np.eye(3)):
	print "Not a rotation matrix R*R^t =!= I"
	sys.exit(0)

     # determine angle of rotation
     s = np.trace(mat)
     angle = np.arccos((s-1)/2.0)
     print "Angle of rotation : ", angle

     # determine axis of rotation
     Evals, Evecs = np.linalg.eig(mat)
     index = list(np.isclose(Evals,1)).index(True)
     print "Axis of rotation : ", np.real(Evecs[:,index])
