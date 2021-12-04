import numpy as np

nbDepth = 66
# generate number of vertices, change [low, high[ parameters to increase or decrease this number
nbVertices = np.random.randint((nbDepth-1)**2, nbDepth**2)

nodes = {}
nodes[0] = [0]
nodes[nbDepth-1] = [nbVertices-1]
edges = []

for i in range(1, nbVertices-1):
    node_class = np.random.choice(3, 1, p=[0.0001, 0.9997, 0.0002])
    if node_class == 0:
        nodes[0].append(i)
    if node_class == 1:
        depth = np.random.randint(1, nbDepth-1)
        if depth not in nodes.keys():
            nodes[depth] = []
        nodes[depth].append(i)
    if node_class == 2:
        nodes[nbDepth-1].append(i)
    
for k, v in sorted(nodes.items()):
    if k < nbDepth-1:
        for node in v:
            from_node = node
            p = np.random.binomial(1, 0.5, nbDepth-k-1)
            possible_depth = np.sum(p) + k + 1
            possible_nodes = []
            for depth in range(k, possible_depth):
                possible_nodes += nodes[depth]
            possible_nodes.remove(node)
            # generate number of edges, change [low, high[ parameters to increase or decrease this number
            nbOfEdges = np.random.randint(len(possible_nodes)//2, len(possible_nodes))
            to_nodes = np.random.choice(possible_nodes, nbOfEdges, replace=False)
            # print(from_node, ":", to_nodes, ", size :",  len(to_nodes))
            for to_node in to_nodes:
                date = np.random.randint(k, (k+1)*2)
                edges.append((from_node, to_node, date, 1))

nbEdges = len(edges)

# Write to file
f = open("g.txt", "w")

f.write(str(nbVertices) + "\n")
f.write(str(nbEdges) + "\n")

for k in nodes.keys():
    for v in nodes[k]:
        f.write(str(v) + "\n")

for edge in edges:
    f.write(str(edge).replace(" ", "") + "\n")

f.close()

for k, v in sorted(nodes.items()):
    print("depth :", k, ", nodes :", v)