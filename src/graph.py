class Graph:
    """
    Graph class that stock our graph with some path finding methods.
    This graph use a dictionnary instead of a list to have the possibility to use string as name of vertices instead of index.
    Then the name of a vertex is the key in our map instead of an index in a list.
    More efficiant btw.
    """

    def __init__(self):
        self.adj = {}
        self.nbVertices = 0
        self.nbEdges = 0
    
    def createFromFile(self, fileName):
        """
        Creating an oriented grpah from a given path.
        Construct each vertex and edge by browsing lines of the file.
        """
        # Recovering lines
        with open(fileName) as f:
            lines = []
            for l in f:
                lines.append(l.rstrip()) # .rstrip() to remove \n

        # Set numbers of components
        self.nbVertices = int(lines[0])
        self.nbEdges = int(lines[1])

        # Adding vertices into our adj
        for v in lines[2:(2 + self.nbVertices)]:
            self.adj[v] = []

        # Adding edges into our adj
        for l in lines[(2 + self.nbVertices):(2 + self.nbVertices) + self.nbEdges]:
            toSplit = l.split(",") # parse lines
            self.addEdge(toSplit[0][1:], toSplit[1], int(toSplit[2]), int(toSplit[3][:-1]))
    
    def createManually(self):
        """
        Asking the user to build the graph himself from the prompt.
        """
        self.nbVertices = int(input("Enter the number of vertices: "))
        self.nbEdges = int(input("Enter the number of edge: "))

        for i in range(self.nbVertices):
            v = input("Enter the name of the vertex number %d/%d: " % (i+1, self.nbVertices))
            self.adj[v] = []
        
        for i in range(self.nbEdges):
            l = input("Enter the edge number %d/%d (as: u v t lambda) : " % (i+1, self.nbEdges))
            toSplit = l.split(" ") # parse lines
            self.addEdge(toSplit[0], toSplit[1], int(toSplit[2]), int(toSplit[3]))

    def addEdge(self, vertex, toEdge, startTime, arrivalTime):
        """
        Putting an edge into our adjacent list which is a dictionnary.
        The vertex is a key, and it value is [the dest vertex, the start time, the end time].
        """
        self.adj[vertex].append([toEdge, startTime, arrivalTime])

    def print(self):
        for k in self.adj:
            print("%s:" % (k))
            for e in self.adj[k]:
                print(" -> %s" % (e))