import heapq
import math

class Graph:
    """
    Graph class that stock our graph with some path finding methods.
    This graph use a dictionnary instead of a list to have the possibility to use string as name of vertices instead of index.
    Then the name of a vertex is the key in our map instead of an index in a list.
    More efficiant btw.
    """

    def __init__(self):
        self.adj = {}
        self.nb_vertices = 0
        self.nb_edges = 0
    
    def create_from_file(self, file_name):
        """
        Creating an oriented grpah from a given path.
        Construct each vertex and edge by browsing lines of the file.
        """
        # Recovering lines
        with open(file_name) as f:
            lines = []
            for l in f:
                lines.append(l.rstrip()) # .rstrip() to remove \n

        # Set numbers of components
        self.nb_vertices = int(lines[0])
        self.nb_edges = int(lines[1])

        # Adding vertices into our adj
        for v in lines[2:(2 + self.nb_vertices)]:
            self.adj[v] = []

        # Adding edges into our adj
        for l in lines[(2 + self.nb_vertices):(2 + self.nb_vertices) + self.nb_edges]:
            to_split = l.split(",") # parse lines
            self.add_edge(to_split[0][1:], to_split[1], int(to_split[2]), int(to_split[3][:-1]))
    
    def create_manually(self):
        """
        Asking the user to build the graph himself from the prompt.
        """
        self.nb_vertices = int(input("Enter the number of vertices: "))
        self.nb_edges = int(input("Enter the number of edge: "))

        for i in range(self.nb_vertices):
            v = input(f"Enter the name of the vertex number {i+1}/{self.nb_vertices}: ")
            self.adj[v] = []
        
        for i in range(self.nb_edges):
            l = input("Enter the edge number %d/%d (as: u v t lambda) : " % (i+1, self.nb_edges))
            to_split = l.split(" ") # parse lines
            self.add_edge(to_split[0], to_split[1], int(to_split[2]), int(to_split[3]))

    def add_edge(self, vertex, to_edge, start_time, arrival_time):
        """
        Putting an edge into our adjacent list which is a dictionnary.
        The vertex is a key, and it value is [the dest vertex, the start time, the end time].
        """
        self.adj[vertex].append((to_edge, start_time, arrival_time))

    def print(self):
        for k in self.adj:
            print(f"{k}:")
            for e in self.adj[k]:
                print(f" -> {e}")

    def dijkstra(self, start, end):
        """
        Complexity in O(E*log(V))
        V number of vertices
        E number of edges
        https://stackoverflow.com/questions/26547816/understanding-time-complexity-calculation-for-dijkstra-algorithm
        """
        dist = {}
        prev = {}
        queue = []
        
        for e in self.adj:
            dist[e] = math.inf
            
        dist[start] = 0
        prev[start] = None
            
        heapq.heappush(queue, (0, start)) # dist is 0 at the start
        
        while queue: # while our queue is not empty
            
            # extract the minimum distance of the queue and remove it           
            _, u = heapq.heappop(queue)
               
            for e in self.adj[u]:
                # e = ('a', 2, 1)
                v = e[0]
                weight = e[1]

                if dist[v] > dist[u] + weight:
                    # assigning new dist for v node
                    dist[v] = dist[u] + weight
                    heapq.heappush(queue, (dist[v], v))
                    # keep parent
                    prev[v] = u
        
        # Backtracking the path
        path = []
        n = end
        while n:
            path.append(n)
            n = prev[n]
        path.reverse()
        
        return dist[end], path
            