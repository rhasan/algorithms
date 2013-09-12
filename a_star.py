from collections import defaultdict

from graph import *
from heapq import *

INPUT_GRAPH_LOCATION = "romania.in"


WHITE = 0 #not explored nodes
GRAY = 1 #in the queue nodes/in processing/exploring
BLACK = 3 #explored nodes

"""
Uniform cost search reference: page 84 Peter Norvig AI book
"""
def uniform_cost_search(problem):
    color = defaultdict(lambda: WHITE)
    distance = defaultdict(lambda: float('inf'))
    path = defaultdict(lambda: None)

    color[problem.initial] = GRAY
    distance[problem.initial] = 0
    path[problem.initial] = None
    heap = []
    initial_state = (0,problem.initial)
    heappush(heap, initial_state)
    
    while heap:
        (pathcost,u) = heappop(heap)
        children_states = problem.children(u)

        for (children,cost) in children_states:
            if color[children] == WHITE:
                color[children] = GRAY
                distance[children] = distance[u] + cost
                heappush(heap, (distance[children],children))

            elif color[children] != WHITE and distance[children] > distance[u] + cost:
                new_cost = distance[u] + cost
                #heapreplace(heap, (distance[children],children),(new_cost,children)) #no replace support in python
        color[children] = BLACK





"""Class for graph search problem"""
class Problem:
    def __init__(self, g,initial,goal):
        self.graph = g
        self.initial = initial
        self.goal = goal

    def goal_test(self,node):
        return goal.node_id == node.node_id

    def children(self,node):
        edges = g.outgoing_edges(node)
        cldrn = list()
        for edg in edges:
            end = edg.end
            cost = edg.label
            cldrn.append((end,cost))
        return cldrn
        

def get_input_graph(file):
    g = Graph()
    node_geo_locations = dict()
    node_label_id_mapping = dict()

    input_graph_file = open(file,"r")
    
    first_line = next(input_graph_file)

    (n,m) = map(int,first_line.split())
    #print n, m

    line_count = 0
    node_id = 1
    for line in input_graph_file:

        (node_label,geo_location) = line.split("=")
        node_label = node_label.strip()
        (geo_x,geo_y) = map(int,geo_location.split(","))
        #print "Node:["+node_label+"], geo x:", geo_x, "geo y:", geo_y

        node = Node(node_id,node_label)
        g.add_node(node)
        node_label_id_mapping[node_label] = node_id
        node_geo_locations[node_id] = (geo_x,geo_y)

        node_id += 1

        line_count += 1
        if(line_count==n):
            break;

    line_count = 0
    for line in input_graph_file:
        (u_node_label,edges) = line.split(":")
        u_node_label = u_node_label.strip()

        edge_list = edges.split(",")
        node_start = g.node(node_label_id_mapping[u_node_label])

        #print "Node:["+u_node_label+"] has edges:"
        for edge in edge_list:
            (v_node_label,cost) = edge.strip().split("=")
            v_node_label = v_node_label.strip()
            cost = int(cost)
                        
            node_end = g.node(node_label_id_mapping[v_node_label])
            edge = Edge(node_start,node_end,cost)
            g.add_edge(edge)

            #print "["+v_node_label+"]", "cost:",cost

        if(line_count==m):
            break;

    return (g,node_geo_locations)

def main():
    (g,geo_locations) = get_input_graph(INPUT_GRAPH_LOCATION)
    g.pretty_print()


if __name__ == "__main__":
    main()