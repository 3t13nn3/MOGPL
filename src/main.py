import sys, time

from graph import Graph

if __name__ == "__main__":
    g = Graph()
    
    if len(sys.argv) == 1:
        g.create_manually()

    else:
        g.create_from_file(sys.argv[1])
    
    # Interval to set the graph on a special time
    interval = [0,1000000000]

    g2 = g.create_simplified(interval)

    start = 'a'
    end = 'l'

    print("-   -   -   -   -   -   -")
    print(f"\x1b[1m\x1b[32mStart: \'{start}\'\x1b[0m | \x1b[1m\x1b[31mEnd \'{end}\'\x1b[0m | On the interval \x1b[1m{interval}\x1b[0m:")
    print("-   -   -   -   -   -   -")

    stime = time.time()
    print("\x1b[1m\x1b[33mEarliest Arrival:\t> ", g2.earliest_arrival(start, end))
    etime = time.time()
    print(etime-stime)
    stime = time.time()
    print("\x1b[1m\x1b[34mLatest Departure:\t> ", g2.latest_departure(start, end))
    etime = time.time()
    print(etime-stime)
    stime = time.time()
    print("\x1b[1m\x1b[35mFastest Path:\t\t> ", g2.fastest_path(start, end))
    etime = time.time()
    print(etime-stime)
    stime = time.time()
    print("\x1b[1m\x1b[36mShortest Path:\t\t> ", g2.shortest_path(start, end))
    etime = time.time()
    print(etime-stime)
    
    print("\x1b[0m-   -   -   -   -   -   -")