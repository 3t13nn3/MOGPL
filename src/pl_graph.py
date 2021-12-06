import sys
import gurobipy as gp

# Check command line and read all lines in txt file
if len(sys.argv) == 2 and sys.argv[1].split('.')[len(sys.argv[1].split('.'))-1] == 'txt':
    with open(sys.argv[1]) as f:
        lines = []
        for l in f:
            # if l.rstrip() not in lines:
            lines.append(l.rstrip())# .rstrip() to remove \n
else:
    print("The file must taken one txt file as argument !")
    exit(-1)

# Create all parameters
VERTICES = int(lines[0])
EDGES = int(lines[1])

# origin = "a"
# destination = "l"
# Testing on test set
origin = "0"
destination = str(VERTICES-1)
# Interval t_alpha and t_omega
sdate = 0
edate = 1000000

edges = gp.tuplelist()
cost = {}

for l in lines[2+VERTICES:len(lines)]:
    l = l.replace('(', '').replace(')', '').split(',')
    from_node = l[0]
    to_node = l[1]
    depart_date = int(l[2])
    travel_time = int(l[3])
    # Adding all necessary edges while verifing depart date and end date
    if (from_node == origin and int(depart_date) >= sdate)\
        or (to_node == destination and int(depart_date) + travel_time <= edate)\
        or (from_node != origin and to_node != destination):
        # if (from_node, to_node, int(depart_date), int(travel_time)) not in edges:
        edges.append((from_node, to_node, int(depart_date), int(travel_time)))
        cost[(from_node, to_node, int(depart_date), int(travel_time))] = 1

# Create model
m = gp.Model()

# Create decision variables
x = m.addVars(edges, vtype=gp.GRB.BINARY, obj=cost, name ="flow")
m.update()

# Add constraints
# Only one arc which leave from the node containing origin can be chosen
m.addConstr(sum(x[i, j, k, l] for i, j, k, l in edges.select(origin, '*', '*', '*')) >= 1)
# Only one arc which arrive in the node containing destination can be chosen
m.addConstr(sum(x[i, j, k, l] for i, j, k, l in edges.select('*', destination, '*', '*')) >= 1)
# If an arc is taken, so its precessor should also be taken
for i, j, k, l in edges:
    if i != origin:
        m.addConstr(x[i, j, k, l] <=\
            sum(x[i_, j_, k_, l_] for i_, j_, k_, l_ in edges.select('*', i, '*', '*') if k >= k_ + l_ ))

# Solve problem
m.optimize()

# Trace path
if m.status == gp.GRB.Status.OPTIMAL:
    print("Run time :", m.Runtime)
    print('The final solution is:')
    for i, j, k, l in edges:
        if(x[i, j, k, l].x > 0):
            print((i, j, k), x[i, j, k, l].x)