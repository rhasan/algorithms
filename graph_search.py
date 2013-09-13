import math
from collections import defaultdict

from graph import *
from priority_queue import CustomPriorityQueue
from stopwatch import StopWatch
from sets import Set

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
    parent = defaultdict(lambda: None)

    color[problem.initial] = GRAY
    distance[problem.initial] = 0
    #parent[problem.initial] = None
    pq = CustomPriorityQueue()
    initial_state = (0,problem.initial)
    pq.add(initial_state)
    
    while pq.empty() == False:
        (pathcost,u) = pq.pop()
        children_states = problem.children(u)

        if problem.goal_test(u):
            return (pathcost,reconstruct_path(parent,problem.goal))

        for (child,cost) in children_states:
            if color[child] == WHITE:
                color[child] = GRAY
                distance[child] = pathcost + cost
                pq.add((distance[child],child))
                parent[child] = u
            elif color[child] == GRAY and distance[child] > pathcost + cost:
                distance[child] = pathcost + cost
                parent[child] = u
                pq.replace(child,(distance[child],child))

        color[u] = BLACK





class ProblemShortestPath:
    """Class for graph search problem"""
    def __init__(self, g, initial, goal):
        self.graph = g
        self.initial = initial
        self.goal = goal

    def goal_test(self,node):
        return self.goal.node_id == node.node_id

    def children(self, node):
        edges = self.graph.outgoing_edges(node)
        cldrn = list()
        for edg in edges:
            end = edg.end
            cost = edg.label
            cldrn.append((end,cost))
        return cldrn

    def init_huristic(self, geo_locations):
        self.geo_locations = geo_locations

    def h(self,p,q):
        (p_x, p_y) = self.geo_locations[p]
        (q_x, q_y) = self.geo_locations[q]
        #return (p_x-q_x)*(p_x-q_x) + (p_y-q_y)*(p_y-q_y)
        return math.hypot((p_x-q_x),(p_y-q_y))
        


def a_star(problem):
    """
    A* search reference: http://en.wikipedia.org/wiki/A*_search_algorithm
    """
    closedset = Set()
    openset = Set()
    parent = defaultdict(lambda: None)
    g = {}
    f = {}

    openset.add(problem.initial)
    g[problem.initial] = 0
    f[problem.initial] = g[problem.initial] + problem.h(problem.initial,problem.goal)

    pq = CustomPriorityQueue()
    pq.add((f[problem.initial],problem.initial))

    while pq.empty() == False:
        (current_f, current) = pq.pop()

        if problem.goal_test(current):
            return (g[current],reconstruct_path(parent,problem.goal))

        openset.remove(current)
        closedset.add(current)

        children = problem.children(current)
        for (child,cost) in children:
            tentative_g_score = g[current] + cost
            if child in closedset and tentative_g_score >= g[child]:
                continue
            if child not in closedset or tentative_g_score < g[child]: # don't need to initialize for each i in g.V: g[i]=inf. The reason is
                                                                       # if a node x is not initilized that means there was visited. 
                                                                       # That means it the node x is not in openset. Hence the node
                                                                       # x is also not in closedset
                parent[child] = current
                g[child] = tentative_g_score
                f[child] = g[child] + problem.h(child,problem.goal)
                #print "edge:",current,"-->",child,"real:",cost, "approx:",problem.h(current,child)
                if child not in openset:
                    openset.add(child)
                    pq.add((f[child],child))
                elif child in openset:
                    # Replace the priority queue f[child] value. Wiki algo didn't use a priority queue. 
                    # They choose the current node by selecting the node in openset having the lowest f[] value
                    # Therefore they are getting the updated f values from f[]. In our case, the lowest f[] value
                    # is taken from the priority queue. Therefore, we need to keep the most uptodate f values in 
                    # the priority queue. The replace operation is optimized according to python documentation.
                    pq.replace(child,(f[child],child))
                    #print "replace"

    return None


def a_star_beam_search(problem,beam_size):
    """
    A* search reference: http://en.wikipedia.org/wiki/A*_search_algorithm
    """
    closedset = Set()
    openset = Set()
    parent = defaultdict(lambda: None)
    g = {}
    f = {}

    openset.add(problem.initial)
    g[problem.initial] = 0
    f[problem.initial] = g[problem.initial] + problem.h(problem.initial,problem.goal)

    pq = CustomPriorityQueue()
    pq.add((f[problem.initial],problem.initial))

    while pq.empty() == False:
        (current_f, current) = pq.pop()

        if problem.goal_test(current):
            #todo path
            return (g[current],reconstruct_path(parent,problem.goal))

        openset.remove(current)
        closedset.add(current)

        children = problem.children(current)
        children_count = 0
        for (child,cost) in children:
            tentative_g_score = g[current] + cost
            if child in closedset and tentative_g_score >= g[child]:
                continue
            if (child not in closedset or tentative_g_score < g[child]) and children_count < beam_size:
                parent[child] = current
                g[child] = tentative_g_score
                f[child] = g[child] + problem.h(child,problem.goal)
                children_count += 1
                if child not in openset:
                    openset.add(child)
                    pq.add((f[child],child))
                elif child in openset:
                    pq.replace(child,(f[child],child))

    return None


def reconstruct_path(parent,current):
    if current in parent:
        p = reconstruct_path(parent,parent[current])
        p.append(current)
        return p
    else:
        return [current]


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
        node_geo_locations[node] = (geo_x,geo_y)

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
    p = ProblemShortestPath(g,g.node(0),g.node(1))

    #uniform cost search
    sw1 = StopWatch()
    (u_cost, result_path) =  uniform_cost_search(p)
    el1 = sw1.elapsed_milliseconds()

    print "Uniform cost search"
    print "Solution:",u_cost
    print "Path:", result_path
    print "Time:", el1

    #A* search
    p.init_huristic(geo_locations)
    sw1.reset()
    (a_cost, result_path) = a_star(p)
    el1 = sw1.elapsed_milliseconds()
    print "===================="
    print "A * search"
    print "Solution:",a_cost
    print "Path:", result_path
    print "Time:", el1    

    #A* search
    sw1.reset()
    beam_size = 3
    (a_cost, result_path) = a_star_beam_search(p,beam_size)
    el1 = sw1.elapsed_milliseconds()
    print "===================="
    print "A * beam search"
    print "Beam size:", beam_size
    print "Solution:",a_cost
    print "Path:", result_path
    print "Time:", el1    


if __name__ == "__main__":
    main()