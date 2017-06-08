
def readOBJ(filename):
    objectVertices = []
    objectNormals = []
    objectFaces = []

    for line in open(filename):
        if line.split():
            line = line.split()

            if line[0] == 'v':
                objectVertices.append(map(float, line[1:]))
            if line[0] == 'vn':
                objectNormals.append(float(line[1:]))

            ###### von hier kroell #######
            if line[0] == 'f':
                #objectFaces.append(map(int, line[1:]))
                first = line[1:]
                print(first)
                for face in first:
                    objectFaces.append(map(float, face.split('//')))
    for face in objectFaces:
        # if no vt is available fill up with 0 at list position 1
        if len(face) == 2:
            face.insert(1, 0.0)
        # if no vt and no vn is available fill up with 0 at list position 1 and 2
        if len(face) == 1:
            face.insert(1, 0.0)
            face.insert(2, 0.0)

    ###### bis hier kroell ###########
    #print (objectVertices)
    #print (objectNormals)
    print (objectFaces)
    return (objectVertices, objectNormals, objectFaces)

def loadOBJ(filename):
    vertices = []
    normals = []
    faces = []

    #print "Loading File: ", sys.argv[1] + "..."

    with open(filename, "r") as file:
        for line in file:
            if line.startswith("v "):
                vertices.append(map(float, line.split()[1:]))
            elif line.startswith("vn "):
                normals.append(map(float, line.split()[1:]))
            elif line.startswith("f "):
                face = []
                for vertex_as_string in line.split()[1:]:
                    vertex_as_string_list = vertex_as_string.split("/")
                    v = int(vertex_as_string_list[0]) - 1
                    t = -1
                    n = -1
                    if len(vertex_as_string_list) > 1 and vertex_as_string_list[1]:
                        t = int(vertex_as_string_list[1]) - 1
                    if len(vertex_as_string_list) > 2 and vertex_as_string_list[2]:
                        n = int(vertex_as_string_list[2]) - 1
                    face.append([v, t, n])
                faces.append(face)
    return (vertices, normals, faces)