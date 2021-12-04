import numpy as np

f = open("g.txt", "w")

nbVertices = 1000000
nbEdges = 4000000

f.write(str(nbVertices) + "\n")
f.write(str(nbEdges) + "\n")

edges = []

for i in range(nbVertices):
    f.write(str(i) + "\n")

for i in range(nbEdges):
    from_node = np.floor((i * (nbVertices/nbEdges))).astype(int)
    to_node = np.random.randint(from_node, nbVertices)
    date = i
    e = "(" + str(from_node) + "," + str(to_node) + "," + str(date) + ",1)" 
    f.write(e + "\n")

f.close()