
class Node:
    """Class for a graph node"""
    def __init__(self,node_id,label):
        self.node_id = node_id
        self.label = label

class Edge(object):
    """Class for a graph edge"""
    def __init__(self, node_u,node_v,label):
        self.node_u = node_u
        self.node_v = node_v
        self.label = label
