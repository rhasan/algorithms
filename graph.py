from collections import defaultdict
"""Class for a graph node"""
class Node:
    """Initializes a node with a node id and label"""
    def __init__(self,node_id,label):
        self.node_id = node_id
        self.label = label
    
    def __key(self):
        return self.node_id

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return self.label

"""Class for a graph edge"""
class Edge:
    """
    Initializes an edge with a start node and end node and a label
    start and end are instances of Node class.
    """
    def __init__(self, start, end,label):
        self.start = start
        self.end = end
        self.label = label

    def __key(self):
        #return (self.start,self.label,self.end) #for multi edge
        return (self.start,self.end) #for single edge per node pair

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return str((self.start.label,self.label,self.end.label))


"""Class for Graphs"""
class Graph(object):
    
    """
    Initializes the graph.
    """
    def __init__(self):
        self.edges = defaultdict(lambda: list())
        self.node_dict = dict()
        #self.nodes_list = list()

    """
    Adds a Node to the graph.
    """
    def add_node(self,node):
        self.node_dict[node.node_id] = node

    """
    Returns the list of Node instances in the graph.
    """
    def node_list(self):
        return self.node_dict.values()

    """
    Adds an Edge to the graph.
    """
    def add_edge(self,edge):
        self.edges[edge.start.node_id].append(edge)

    """
    Returns the Node for the node_id.
    """
    def node(self,node_id):
        return self.node_dict[node_id]

    """
    Returns the list of outgoing edges from node.
    """
    def outgoing_edges(self,node):
        return self.edges[node.node_id]

    """
    Returns the list adjacent nodes
    """
    def adjacent(self,node):
        adj = list()
        edgs = self.edges[node.node_id]
        for edg in edgs:
            adj.append(edg.end)
        return adj

    """
    Returns the number of nodes in the graph.
    """
    def size(self):
        return len(self.node_dict)

    """
    Print the graph.
    """
    def pretty_print(self):
        nodes = self.node_list()

        for node in nodes:
            if len(self.edges[node.node_id])>0:
                print "Outgoing edges from node", node, ":"
            for edge in self.edges[node.node_id]:
                print edge

        