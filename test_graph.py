import graph_search as gs
from graph import *
(g,geo_locations) = gs.input_graph_undirected("romania.in")
(g1,geo_locations1) = gs.input_graph_undirected("romania.in")
print g==g1

m = {}
m[g] = 1
m[g1] = 2
print m

node = Node(100,"test")
g.add_node(node,True)

node1 = Node(101,"test1")
g.add_node(node1,True)

edge = Edge(node,120,node1)

print g==g1

