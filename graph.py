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
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.__key()==other.__key()

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
        return (self.start,self.label,self.end) #for multi edge
        #return (self.start,self.end) #for single edge per node pair

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return str((self.start.label,self.label,self.end.label))
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.__key()==other.__key()

class Graph(object):
    """Class for Graphs"""
    
    def __init__(self):
        """
        Initializes the graph.
        """
        self.edges = defaultdict(lambda: list())
        self.node_dict = dict()
        self.key = None

    def add_node(self,node,update_key=False):
        """
        Adds a Node to the graph.
        """
        self.node_dict[node.node_id] = node
        if update_key:
            self.__update_key()

    def node_list(self):
        """
        Returns the list of Node instances in the graph.
        """
        return self.node_dict.values()

    def add_edge(self,edge,update_key=False):
        """
        Adds an Edge to the graph.
        """
        self.edges[edge.start].append(edge)
        if update_key:
            self.__update_key()

    def node(self,node_id):
        """
        Returns the Node for the node_id.
        """
        return self.node_dict[node_id]

    def outgoing_edges(self,node):
        """
        Returns the list of outgoing edges from node.
        """
        return self.edges[node]

    def adjacent(self,node):
        """
        Returns the list adjacent nodes
        """
        adj = list()
        edgs = self.edges[node]
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
            if len(self.edges[node])>0:
                print "Outgoing edges from node", node, ":"
            for edge in self.edges[node]:
                print edge


    def __key(self):
        if self.key == None:
            self.__update_key()
        return self.key

    def __hash__(self):
        return self.__key()
    
    def __eq__(self, other):
        if other is None:
            return False
        return self.__key()==other.__key()

    def __update_key(self):
        tripl_list = []
        for node in self.edges:
            edge_list = self.edges[node]
            tripl_list.extend(map(str,edge_list))

        nodes = self.node_list()
        node_list = map(str,nodes)
        merge_list = tripl_list + node_list
        merge_list.sort()
        self.key = hash(tuple(merge_list))
        #print self.key
#graph has key:
# an equality check using the has of sorted list of all the triples represented by a graph
# e.g In [96]: ll3=['python is cool','java is cool']

# ll4 = ['java is cool','python is cool']

# ll3.sort()

# ll4.sort()

# ll3
# ['java is cool', 'python is cool']

# ll4
# ['java is cool', 'python is cool']

# hash(str(ll3))==hash(str(ll4))
# True
# hash(tuple(ll3))==hash(tuple(ll4))
# True

# t1 = tuple(ll3)

# t2 = tuple(ll4)

# t1
# ('java is cool', 'python is cool')

# t2
# ('java is cool', 'python is cool')

# h = {}

# h[t1]=1

# h
# {('java is cool', 'python is cool'): 1}

# h[t2]=2

# h
# {('java is cool', 'python is cool'): 2}

        