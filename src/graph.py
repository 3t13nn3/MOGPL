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
        Creating an oriented graph from a given path.
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
        for l in lines[(2 + self.nb_vertices):(2 + self.nb_vertices) + self.nb_edges + 1]:
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
             
        for e in self.adj:
            node = e.split(",") # node[0] = a, node[1] = 1
            if node[0] == start:
                dist[e] = 0
                prev[e] = None
                heapq.heappush(queue, (0, e)) # dist is 0 at the start
            
        
        
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
        
        tmp = math.inf
        end_name = ""
        for e in self.adj:
            node = e.split(",") # node[0] = a, node[1] = 1
            if node[0] == end:
                if dist[e] < tmp:
                    tmp = dist[e]
                    end_name = e

        # Backtracking the path
        path = []
        
        n = end_name
        while n:
            path.append(n)
            n = prev[n]
        path.reverse()
        
        return dist[end_name], path
    
    def add_edge_simplified(self, vertex, to_edge, weight):
        """
        Same method as above wityh only a weight
        """
        self.adj[vertex].append((to_edge, weight))
        
    def create_simplified(self):
        g = Graph()
        vIn = {}
        vOut = {}
        v = {}
        
        for e in self.adj:
            # using set for unicity (we don't want multiple time the same departur date)
            vOut[e] = set()
            vIn[e] = set()
        
        for k in self.adj:
            # k = a, b ,c ....
            for e in self.adj[k]:
                # ('b', 2, 1)   
                print(e[1])
                vIn[e[0]].add(e[1] + 1)
                vOut[k].add(e[1])  

        
        for k in vIn:
            v[k] = set()
            while len(vIn[k]) != 0 and len(vOut[k]) != 0 and min(vIn[k]) > min(vOut[k]):
                vOut[k].remove(min(vOut[k]))
                        
            v[k] = sorted(vIn[k].union(vOut[k]))
            
            #print(v[k])
            
            tmp = None
            # get first element of the set
            first = None
            for e in v[k]:
                first = e
                break
            
            for e in v[k]:
                g.adj[k + "," + str(e)] = []
                if e != first:
                    g.add_edge_simplified(k + "," + str(tmp), k + "," + str(e), 0)
                tmp = e
            
        # for all nodes in our new graphs as a,1 a,2 a,3
        for e in g.adj:
            node = e.split(",") # node[0] = a, node[1] = 1

            tmp = ''
            # for all decendent of our node in the original graph 'a'
            for f in self.adj[node[0]]:
                
                # 'b' or 'c'
                if tmp != f[0]:
                    tmp = f[0]
                    #print(f)
                    current_weight = int(node[1])
                    # if the weight of the node exist in vIn of the letter f[0]
                    if current_weight + 1 in vIn[f[0]]:
                        g.add_edge_simplified(e, f[0] + ',' + str(current_weight + 1), 1)   
        
        return g
        
