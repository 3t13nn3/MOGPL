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
destination = 'l'

links = gp.tuplelist()
nodes = []
cost = {}
date = {}

for n in lines[2:2+VERTICES]:
    nodes.append(n)
    
for l in lines[2+VERTICES:len(lines)]:
    l = l.replace('(', '').replace(')', '').split(',')
    from_node = l[0]
    to_node = l[1]
    depart_date = int(l[2])
    travel_cost = int(l[3])
    links.append((from_node, to_node, int(depart_date)))
    date[(from_node, to_node, int(depart_date))] = int(depart_date)
    cost[(from_node, to_node, int(depart_date))] = int(travel_cost)

# print("links : ", links)
# print("date :", date)
# print("cost :", cost)

# Create model
m = gp.Model()

# Create decision variables
x = m.addVars(links, vtype=gp.GRB.BINARY, obj=cost, name ="flow")
m.update()

# Add constraints
# Only one arc which leave from the node containing origin can be chosen
# m.addConstr(-sum(x[i, j, k] for i, j, k in links.select(origin, '*', '*')) <= -1)
# # Only one arc which arrive in the node containing destination can be chosen
# m.addConstr(-sum(x[i, j, k] for i, j, k in links.select('*', destination, '*')) <= -1)
# # One arc between every nodes between node containing origin and destination
# for node in nodes:
#     if node != origin and node != destination:
#         m.addConstr(
#             sum(x[i, j, k] for i, j, k in links.select(node, '*', '*'))\
#             - sum(x[i_, j_, k_] for i_, j_, k_ in links.select('*', node, '*'))\
#             <= 2)
# date+1 of the previous node should be lower than the current date
for node in nodes:
    for i, j, k in links.select(node, '*', '*'):
        for i_, j_, k_ in links.select(j, '*', '*'):
            m.addConstr( x[i, j, k]*date[i, j, k]\
            - x[i_, j_, k_]*date[i_,j_,k_]\
                <= 5) # à changer, 5 vient de nul part mais marche sur a -> l, pas sur tous les chemins

for node in nodes:
    m.addConstr( sum(x[i, j, k] for i, j, k in links.select(node, '*', '*'))\
                - sum(x[j, i, k] for j, i, k in links.select('*', node, '*')) == 
                (1 if node == origin else -1 if node == destination else 0 ),'node%s_' % node )


# Solve problem
m.optimize()

# Trace path
if m.status == gp.GRB.Status.OPTIMAL:
    print('The final solution is:')
    for i, j, k in links:
        # if(x[i, j, k].x > 0):
        print((i, j, k), x[i, j, k].x)