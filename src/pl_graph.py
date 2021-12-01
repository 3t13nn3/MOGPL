import sys
import gurobipy as gp

# Check command line and read all lines in txt file
if len(sys.argv) == 2 and sys.argv[1].split('.')[1] == 'txt':
    with open(sys.argv[1]) as f:
        lines = []
        for l in f:
            lines.append(l.rstrip()) # .rstrip() to remove \n
else:
    print("The file must taken one txt file as argument !")
    exit(-1)

# Create all parameters
VERTICES = int(lines[0])
EDGES = int(lines[1])

origin = 'a'
destination = 'k'
sdate = 3
edate = 20

links = gp.tuplelist()
cost = {}
    
for l in lines[2+VERTICES:len(lines)]:
    l = l.replace('(', '').replace(')', '').split(',')
    from_node = l[0]
    to_node = l[1]
    depart_date = int(l[2])
    travel_cost = int(l[3])
    if (from_node == origin and int(depart_date) >= sdate)\
        or (to_node == destination and int(depart_date) <= edate)\
        or (from_node != origin and to_node != destination):
        links.append((from_node, to_node, int(depart_date)))
        cost[(from_node, to_node, int(depart_date))] = int(travel_cost)

# Create model
m = gp.Model()

# Create decision variables
x = m.addVars(links, vtype=gp.GRB.BINARY, obj=cost, name ="flow")
m.update()

# Add constraints
# Only one arc which leave from the node containing origin can be chosen
m.addConstr(sum(x[i, j, k] for i, j, k in links.select(origin, '*', '*')) >= 1)
# Only one arc which arrive in the node containing destination can be chosen
m.addConstr(sum(x[i, j, k] for i, j, k in links.select('*', destination, '*')) >= 1)
# If an arc is taken, so its precessor should also be taken
for i, j, k in links:
    if i != origin:
        m.addConstr(x[i, j, k] <= sum(x[i_, j_, k_] for i_, j_, k_ in links.select('*', i, '*') if k >= k_+1 ))

# Solve problem
m.optimize()

# Trace path
if m.status == gp.GRB.Status.OPTIMAL:
    print('The final solution is:')
    for i, j, k in links:
        # if(x[i, j, k].x > 0):
        print((i, j, k), x[i, j, k].x)