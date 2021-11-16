import sys

from graph import Graph

if __name__ == "__main__":
    g = Graph()
    
    if len(sys.argv) == 1:
        g.createManually()

    else:
        g.createFromFile(sys.argv[1])
    
    g.print()