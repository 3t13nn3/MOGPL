import sys

from graph import Graph

if __name__ == "__main__":
    g = Graph()
    
    if len(sys.argv) == 1:
        g.create_manually()

    else:
        g.create_from_file(sys.argv[1])
    
    
    g2 = g.create_simplified()
    
    # g2.print()
    start = 'a'
    end = 'k'

    print("-   -   -   -   -   -   -")
    print(f"\x1b[1m\x1b[32mStart: \'{start}\'\x1b[0m | \x1b[1m\x1b[31mEnd \'{end}\'\x1b[0m:")
    print("-   -   -   -   -   -   -")
    print("\x1b[1m\x1b[34mLatest Departure:\t> ", g2.latest_departure(start, end))
    print("\x1b[1m\x1b[33mEarliest Arrival:\t> ", g2.earliest_arrival(start, end))
    print("\x1b[1m\x1b[36mShortest Path:\t\t> ", g2.shortest_path(start, end))
    print("\x1b[0m-   -   -   -   -   -   -")
