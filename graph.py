from collections import defaultdict

class Node:
    """Class for a graph node"""
    def __init__(self,node_id,label):
        """
        Initializes a node with a node id and label
        """
        self.node_id = node_id
        self.label = label
    
    def __key(self):
        return self.node_id

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return self.label


class Edge:
    """Class for a graph edge"""
    
    def __init__(self, start, end,label):
        """
        Initializes an edge with a start node and end node and a label
        start and end are instances of Node class.
        """
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


class Graph(object):
    """Class for Graphs"""
    
    def __init__(self):
        """
        Initializes the graph.
        """
        self.edges = defaultdict(lambda: list())
        self.node_dict = dict()

    def add_node(self,node):
        """
        Adds a Node to the graph.
        """
        self.node_dict[node.node_id] = node

    def node_list(self):
        """
        Returns the list of Node instances in the graph.
        """
        return self.node_dict.values()

    def add_edge(self,edge):
        """
        Adds an Edge to the graph.
        """
        self.edges[edge.start.node_id].append(edge)

    def node(self,node_id):
        """
        Returns the Node for the node_id.
        """
        return self.node_dict[node_id]

    def outgoing_edges(self,node):
        """
        Returns the list of outgoing edges from node.
        """
        return self.edges[node.node_id]

    def adjacent(self,node):
        """
        Returns the list adjacent nodes
        """
        adj = list()
        edgs = self.edges[node.node_id]
        for edg in edgs:
            adj.append(edg.end)
        return adj

    def size(self):
        """
        Returns the number of nodes in the graph.
        """
        return len(self.node_dict)

    def pretty_print(self):
        """
        Print the graph.
        """
        nodes = self.node_list()

        for node in nodes:
            if len(self.edges[node.node_id])>0:
                print "Outgoing edges from node", node, ":"
            for edge in self.edges[node.node_id]:
                print edge

        