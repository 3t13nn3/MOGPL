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
        self.__adj = {}
        self.__nb_vertices = 0
        self.__nb_edges = 0
    
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
        self.__nb_vertices = int(lines[0])
        self.__nb_edges = int(lines[1])

        # Adding vertices into our adj
        for v in lines[2:(2 + self.__nb_vertices)]:
            self.__adj[v] = []

        # Adding edges into our adj
        for l in lines[(2 + self.__nb_vertices):(2 + self.__nb_vertices) + self.__nb_edges + 1]:
            to_split = l.split(",") # parse lines
            self.__add_edge(to_split[0][1:], to_split[1], int(to_split[2]), int(to_split[3][:-1]))
    
    def create_manually(self):
        """
        Asking the user to build the graph himself from the prompt.
        """
        self.__nb_vertices = int(input("Enter the number of vertices: "))
        self.__nb_edges = int(input("Enter the number of edge: "))

        for i in range(self.__nb_vertices):
            v = input(f"Enter the name of the vertex number {i+1}/{self.__nb_vertices}: ")
            self.__adj[v] = []
        
        for i in range(self.__nb_edges):
            l = input("Enter the edge number %d/%d (as: u v t lambda) : " % (i+1, self.__nb_edges))
            to_split = l.split(" ") # parse lines
            self.__add_edge(to_split[0], to_split[1], int(to_split[2]), int(to_split[3]))

    def __add_edge(self, vertex, to_edge, start_time, arrival_time):
        """
        Putting an edge into our adjacent list which is a dictionnary.
        The vertex is a key, and it value is [the dest vertex, the start time, the end time].
        """
        self.__adj[vertex].append((to_edge, start_time, arrival_time))

    def print(self):
        for k in self.__adj:
            print(f"{k}:")
            for e in self.__adj[k]:
                print(f" -> {e}")

    def __dijkstra(self, start, end, dist, prev):
        current_start = None
        start_find = False
        for e in self.__adj:
            if not e[0] in dist:
                dist[e[0]] = {}
            if e[0] == start and not start_find:
                dist[e[0]][e[1]] = 0
                prev[e] = None
                current_start = e
                start_find = True
            else:
                dist[e[0]][e[1]] = math.inf

        if end not in dist:
            return []

        possible_end = []
        
        if not current_start:
            return []

        for e in self.__adj:
            if e[0] == end:
                possible_end.append(e)

        queue = []

        heapq.heappush(queue, (0, current_start))
        # check if queue is empty or if all targeted end nodes have been browsed and dist marked
        while queue:
            if all(dist[end][e] != math.inf for e in dist[end]):
                break
            # extract the minimum distance of the queue and remove it           
            _, u = heapq.heappop(queue)
            for e in self.__adj[u]:
                v = e
                weight = e[1]
                #print(u[0])
                if dist[v[0][0]][v[0][1]] > dist[u[0]][u[1]] + weight:
                    # assigning new dist for v node

                    dist[v[0][0]][v[0][1]] = dist[u[0]][u[1]] + weight
                    heapq.heappush(queue, (dist[v[0][0]][v[0][1]], v[0]))
                    # keep parent
                    prev[v[0]] = u

    def __BFS(self, start, end, dist, prev):
        for e in self.__adj:
            if not e[0] in dist:
                dist[e[0]] = {}
            if e[0] == start:
                dist[e[0]][e[1]] = 0
                prev[e] = None
                continue
            dist[e[0]][e[1]] = math.inf 
        
        if end not in dist:
            return []

        for u in self.__adj:
            # don't need to check not visited node because we don't know
            # how to reach them
            if dist[u[0]][u[1]] != math.inf:
                # for each childs
                for e in self.__adj[u]:
                    v = e
                    weight = e[0][1]
                    # relaxation
                    if dist[v[0][0]][v[0][1]] > dist[u[0]][u[1]] + (weight - u[1]):
                        dist[v[0][0]][v[0][1]] = dist[u[0]][u[1]] + (weight - u[1])
                        # keep parents for the path
                        prev[v[0]] = u
            

    def __back_tracking(self, node, prev):
        path = []

       # if node == None: #if we havent find an arrival
        #    return []
        while node :
            #print(node)
            path.append(node)
            current = node
            tmp = node
            while tmp[0] == current[0]:
                node = prev[node] 
                if node == None:
                    break
                current = node
        path.reverse()

        return path

    # Dijkstra but we take the lowest time end node as end
    def earliest_arrival(self, start, end):
        
        dist = {}
        prev = {}

        self.__BFS(start, end, dist, prev)

        if end not in dist:
            return []

        # retrieve the lowest end in time
        n = None
        for e in dist[end]:
            if dist[end][e] != math.inf:
                n = (end, e)
                break
        
        return self.__back_tracking(n, prev)
                
    
    # BFS 
    def latest_departure(self, start, end):
        dist = {}
        prev = {}
        
        
        self.__BFS(start, end, dist, prev)

        path = [(0,-1)]

        if end not in dist:
            return []

        for e in dist[end]:    
            #recovery name to pass to previous
            end_name = (end, e)
            if dist[end][e] != math.inf:       
                tmp = self.__back_tracking(end_name, prev)
                
                if tmp[0][1] > path[0][1]:
                    path = tmp
                # checking if we can arrive earlier with the current start
                elif path == tmp[0][1]:
                    if tmp[-1][1] > path[-1][1]:
                        path = tmp

        if path == [(0,-1)]:
            return []

        return path
    
    # BFS
    def fastest_path(self, start, end):
        dist = {}
        prev = {}

        self.__BFS(start, end, dist, prev)

        if end not in dist:
            return []

        end_name = (end, min(dist[end], key=dist[end].get))

        if all(dist[end][e] == math.inf for e in dist[end]):
            return []

        # Backtracking the path and skip useless inter-state of the same node name
        path = self.__back_tracking(end_name, prev)
        final_dist = dist[end][end_name[1]]

        return path, final_dist


    def shortest_path(self, start, end):

        dist = {}
        prev = {}   

        self.__dijkstra(start, end, dist, prev)
        
        if end not in dist:
            return []

        if all(dist[end][e] == math.inf for e in dist[end]):
            return []
        # picking the lowest dist 
        end_name = (end, min(dist[end], key=dist[end].get))
        
        final_dist = dist[end][end_name[1]]

        return self.__back_tracking(end_name, prev), final_dist
    
    def __add_edge_simplified(self, vertex, to_edge, weight):
        """
        Same method as above wityh only a weight
        """
        self.__adj[vertex].append((to_edge, weight))
        
    def create_simplified(self, interval):
        g = Graph()
        v_in = {}
        v_out = {}
        v = {}
        
        for e in self.__adj:
            # using set for unicity (we don't want multiple time the same departur date)
            v_out[e] = set()
            v_in[e] = set()

        for k in self.__adj:
            # k = a, b ,c ....
            for e in self.__adj[k]:
                if (e[1]) >= interval[0] and (e[1] + e[2]) <= interval[1]:
                    v_in[e[0]].add(e[1] + e[2])
                    v_out[k].add(e[1])  

        
        for k in v_in:
            
            #v[k] = set()
            v[k] = sorted(v_in[k].union(v_out[k]))
            
            tmp = None
            # get first element of the set
            first = None
            for e in v[k]:
                first = e
                break
            
            for e in v[k]:
                g.__adj[(k, e)] = []
                if e != first:
                    g.__add_edge_simplified((k, tmp), (k, e), 0)
                tmp = e

        # for all nodes in our new graphs as a,1 a,2 a,3
        for e in g.__adj:
            #print(e)
            tmp = ''
            # for all decendent of our node in the original graph 'a'
            for f in self.__adj[e[0]]:
                #print('\t', f)
                # 'b' or 'c'
                if tmp != f[0]:
                    #print('\t\t', tmp)
                    tmp = f[0]
                    current_weight = e[1] + f[2]
                    # if the weight of the node exist in v_in of the letter f[0]
                    if current_weight in v_in[f[0]] and current_weight - f[2] in v_out[e[0]]:
                        #v_in[f[0]].remove(current_weight)
                        #print("\t\t\t",f[0], v_in[f[0]])
                        g.__add_edge_simplified(e, (f[0], current_weight), 1)   
        
        return g
        
