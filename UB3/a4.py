import numpy as np



def checkRotationMatrix(file):
    print(np.loadtxt(file))
    #print(open(file).read().split())

def matrixInfo(file):
    pass

def main():
    filelist = ["mat1.dat", "mat2.dat"]


    for file in filelist:
        if checkRotationMatrix(file):
            matrixInfo(file)
        else:
            print(file + " ist keine Rotationsmatrix" )


if __name__ == '__main__':
    main()