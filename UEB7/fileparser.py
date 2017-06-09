def readOBJ(filename):
    """Liest eine .obj Datei ein und liefert die vertices, normals, faces zurueck"""
    vertices = []
    normals = []
    faces = []

    for line in open(filename):
        line = line.split()
        if line:
            if line[0] == 'v':
                vertices.append(map(float, line[1:]))
            elif line[0] == 'vn':
                normals.append(map(float, line[1:]))
            elif line[0] == 'f':
                face = []

                for vertexString in line[1:]:
                    vertexList = vertexString.split("/")
                    v = int(vertexList[0]) - 1
                    t = -1
                    n = -1
                    if len(vertexList) > 1 and vertexList[1]:
                        t = int(vertexList[1]) - 1
                    if len(vertexList) > 2 and vertexList[2]:
                        n = int(vertexList[2]) - 1
                    face.append([v, t, n])
                faces.append(face)

    return (vertices, normals, faces)
