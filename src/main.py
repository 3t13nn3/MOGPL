import sys

from graph import Graph

if __name__ == "__main__":
    g = Graph()
    
    if len(sys.argv) == 1:
        g.create_manually()

    else:
        g.create_from_file(sys.argv[1])
    
    g.print()
    
    print(g.dijkstra('a', 'i'))