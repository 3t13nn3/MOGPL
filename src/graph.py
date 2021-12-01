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

    def _dijkstra(self, start, dist, prev, possible_end):

        queue = []
        possible_end = []

        for e in self.adj:
            dist[e] = math.inf

        dist[start] = 0

        heapq.heappush(queue, (0, start))

        # check if queue is empty or if all targeted end nodes have been browsed and dist marked
        while queue or not all(dist[e] != math.inf for e in possible_end):
            
            # extract the minimum distance of the queue and remove it           
            _, u = heapq.heappop(queue)

            for e in self.adj[u]:
                v = e[0]
                weight = e[1]
                
                if dist[v] > dist[u] + weight:
                    # assigning new dist for v node
                    dist[v] = dist[u] + weight
                    heapq.heappush(queue, (dist[v], v))
                    # keep parent
                    prev[v] = u

    def _back_tracking(self, node, prev):
        path = []

       # if node == None: #if we havent find an arrival
        #    return []
        while node:
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
        possible_end = []

        # Fidning the start node
        current_start = None
        for e in self.adj:
            if e[0] == start: # check both if the node is the right
                current_start = e
                prev[e] = None
                break # we could take the first
        
        if not current_start:
            return []

        for e in self.adj:
            if e[0] == end:
                possible_end.append(e)

        self._dijkstra(current_start, dist, prev, possible_end)

        # retrieve the lowest end in time
        n = None
        for e in self.adj:
            if e[0] == end and dist[e] != math.inf:
                n = e
                break
        
        return self._back_tracking(n, prev)
                
    
    # Dijkstra from all departure nodes. Test from the bigger to the last if we can reach arrival if we have one, then cut
    def latest_departure(self, start, end):
        # recovery all the nodes to start with 
        start_nodes = []
        for e in self.adj:
            if e[0] == start: # check if the node is the right
                start_nodes.append(e)

        end_name = None
        current_start = None

        # keep the end we wan reach
        possible_end = []
        prev = {}

        while end_name == None and len(start_nodes) != 0:
            current_start = start_nodes[-1]
            possible_end.append(current_start)
            # remove the current start from our start list
            start_nodes = start_nodes[:-1]
            dist = {}
            prev = {}
            prev[current_start] = None
            self._dijkstra(current_start, dist, prev, possible_end)
            
            # checking if we got a path to our arrival node (if the node dist isn't +inf)
            for e in self.adj:
                if e[0] == end and dist[e] != math.inf:
                    end_name = e
                    break
        
        return self._back_tracking(end_name, prev)
    
    # lowest durée(P) = fin(P) - début(P)
    # mix of earliest arrival and latest_departure
    # Bellman-Ford
    def fastest_path(self, start, end):
        dist = {}
        prev = {}

        for e in self.adj:
            if e[0] == start:
                dist[e] = 0
                prev[e] = None
                continue
            dist[e] = math.inf

        # We loop n-1x through all nodes
        for i in range (0, len(self.adj) - 1):
            # to compare them to there childs
            for u in self.adj:
                # don't need to check not visited node because we don't know
                # how to reach them
                if dist[u] != math.inf:
                    # for each childs
                    for e in self.adj[u]:
                        # print(e[0][1])
                        #print(u)
                        v = e[0]
                        weight = e[0][1]
                        # relaxation
                        if dist[v] > dist[u] + (weight - u[1]):
                            dist[v] = dist[u] + (weight - u[1])
                            # keep parents for the path
                            prev[v] = u

        # picking the lowest dist 
        tmp = math.inf
        end_name = None
        for e in self.adj:
            if e[0] == end:
                if dist[e] < tmp:
                    tmp = dist[e]
                    end_name = e



        if end_name == None: #if we havent find an arrival
            return []
        
        # Backtracking the path and skip useless inter-state of the same node name
        path = self._back_tracking(end_name, prev)

        final_dist = dist[end_name]

        return path, final_dist


    def shortest_path(self, start, end):

        dist = {}
        prev = {}
        possible_end = []

        # Fidning the start node
        current_start = None
        for e in self.adj:
            if e[0] == start: # check both if the node is the right
                current_start = e
                prev[e] = None
                break # we could take the first
        
        if not current_start:
            return []
        
        for e in self.adj:
            if e[0] == end:
                possible_end.append(e)

        self._dijkstra(current_start, dist, prev, possible_end)

        # picking the lowest dist 
        tmp = math.inf
        end_name = None
        for e in self.adj:
            if e[0] == end:
                if dist[e] < tmp:
                    tmp = dist[e]
                    end_name = e

        if not end_name:
            return []

        final_dist = dist[end_name]

        return self._back_tracking(end_name, prev), final_dist
    
    def add_edge_simplified(self, vertex, to_edge, weight):
        """
        Same method as above wityh only a weight
        """
        self.adj[vertex].append((to_edge, weight))
        
    def create_simplified(self, interval):
        g = Graph()
        v_in = {}
        v_out = {}
        v = {}
        
        for e in self.adj:
            # using set for unicity (we don't want multiple time the same departur date)
            v_out[e] = set()
            v_in[e] = set()

        for k in self.adj:
            # k = a, b ,c ....
            for e in self.adj[k]:
                
                # ('b', 2, 1)   
                print(e[0], e[1], e[2])

                #MODIF LAMBDA
                # v_in[e[0]].add(e[1] + 1)
                if (e[1]) >= interval[0] and (e[1] + e[2]) <= interval[1]:
                    v_in[e[0]].add(e[1] + e[2])
                    v_out[k].add(e[1])  

        
        for k in v_in:
            v[k] = set()
            #while len(v_in[k]) != 0 and len(v_out[k]) != 0 and min(v_in[k]) > min(v_out[k]):
            #    v_out[k].remove(min(v_out[k]))
                        
            v[k] = sorted(v_in[k].union(v_out[k]))
            
            #print(v[k])
            
            tmp = None
            # get first element of the set
            first = None
            for e in v[k]:
                first = e
                break
            
            for e in v[k]:
                g.adj[(k, e)] = []
                if e != first:
                    g.add_edge_simplified((k, tmp), (k, e), 0)
                tmp = e

        # for all nodes in our new graphs as a,1 a,2 a,3
        for e in g.adj:
            tmp = ''
            
            # for all decendent of our node in the original graph 'a'
            for f in self.adj[e[0]]:
                
                # 'b' or 'c'
                if tmp != f[0]:
                    #print(f)
                    tmp = f[0]
                    
                    '''
                    LAMBDA MODIF
                    current_weight = int(e[1])
                    # if the weight of the node exist in v_in of the letter f[0]
                    
                    if current_weight + 1 in v_in[f[0]]:
                        #####CHECK FOR A BETTER SOLUTION
                        v_in[f[0]].remove(current_weight + 1)

                        g.add_edge_simplified(e, (f[0], current_weight + 1), 1)
                    '''
                    current_weight = e[1] + f[2]
                    # if the weight of the node exist in v_in of the letter f[0]
                    #print(current_weight)
                    if current_weight in v_in[f[0]]:
                        #####CHECK FOR A BETTER SOLUTION
                        v_in[f[0]].remove(current_weight)

                        g.add_edge_simplified(e, (f[0], current_weight), 1)   
        
        return g
        
