from collections import defaultdict

from graph import *
from priority_queue import CustomPriorityQueue

INPUT_GRAPH_LOCATION = "romania.in"


WHITE = 0 # NOT explored nodes
GRAY = 1  # in the queue/in processing/exploring
BLACK = 3 # explored nodes


def uniform_cost_search(problem):
    """
    Uniform cost search reference: page 84 Peter Norvig AI book
    """
    color = defaultdict(lambda: WHITE)
    distance = defaultdict(lambda: float('inf'))
    path = defaultdict(lambda: None)

    color[problem.initial] = GRAY
    distance[problem.initial] = 0
    path[problem.initial] = None
    pq = CustomPriorityQueue()
    initial_state = (0,problem.initial)
    pq.add(initial_state)
    
    while pq.empty() == False:
        (pathcost,u) = pq.pop()
        children_states = problem.children(u)

        if problem.goal_test(u):
            return pathcost

        for (child,cost) in children_states:
            if color[child] == WHITE:
                color[child] = GRAY
                distance[child] = pathcost + cost
                pq.add((distance[child],child))
            elif color[child] == GRAY and distance[child] > pathcost + cost:
                distance[child] = pathcost + cost
                pq.replace(child,(distance[child],child))

        color[u] = BLACK





class Problem:
    """Class for graph search problem"""
    def __init__(self, g,initial,goal):
        self.graph = g
        self.initial = initial
        self.goal = goal

    def goal_test(self,node):
        return self.goal.node_id == node.node_id

    def children(self,node):
        edges = self.graph.outgoing_edges(node)
        cldrn = list()
        for edg in edges:
            end = edg.end
            cost = edg.label
            cldrn.append((end,cost))
        return cldrn
        

def input_graph_undirected(file):
    g = Graph()
    node_geo_locations = dict()
    node_label_id_mapping = dict()

    input_graph_file = open(file,"r")
    
    first_line = next(input_graph_file)

    (n,m) = map(int,first_line.split())
    #print n, m

    line_count = 0
    node_id = 0
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

            edge_undirected = Edge(node_end,node_start,cost)
            g.add_edge(edge_undirected)
            #print "["+v_node_label+"]", "cost:",cost

        if(line_count==m):
            break;

    return (g,node_geo_locations)

def main():
    (g,geo_locations) = input_graph_undirected(INPUT_GRAPH_LOCATION)
    #g.pretty_print()
    p = Problem(g,g.node(0),g.node(1))

    cost =  uniform_cost_search(p)

    print cost


if __name__ == "__main__":
    main()