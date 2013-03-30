# Follows NetworkX closely.  Stripped down for speed and specialized for my
# application.

from itertools import count
from array import array


class Graph(object):

    def __iter__(self):
        return iter(self.node)

    def __contains__(self, n):
        try:
            return n in self.node
        except TypeError:
            return False

    def __len__(self):
        return len(self.node)

    def __getitem__(self, n):
        return self.node[n]


class DirectedGraph(Graph):

    def __init__(self):
        self.node = {}
        self.pred = {}
        self.succ = {}

    def __eq__(self, other):
        return self.node == other.node and self.pred == other.pred and self.succ == other.succ

    def add_node(self, n, **attr):
        # Will silently overwrite attr if n already exists.
        self.node[n] = attr

    def add_edge(self, u, v):
        if u not in self.succ:
            self.succ[u] = array('I')
            self.pred[u] = array('I')

        if v not in self.succ:
            self.succ[v] = array('I')
            self.pred[v] = array('I')

        if v not in self.succ[u]:
            self.succ[u].append(v)

        if u not in self.pred[v]:
            self.pred[v].append(u)

    def edges(self):
        nodes_nbrs = self.succ.items()
        for n, nbrs in nodes_nbrs:
            for nbr in nbrs:
                yield n, nbr

    def predecessors(self, n):
        return list(self.pred[n])

    def successors(self, n):
        return list(self.succ[n])

    def extract_edges(self, n):
        graph = self.__class__()

        graph.node[n] = self.node[n]

        for u in self.succ[n]:
            graph.node[u] = self.node[u]
            graph.add_edge(n, u)

        for v in self.pred[n]:
            graph.node[v] = self.node[v]
            graph.add_edge(v, n)

        return graph


def node_link_data(graph):
    mapping = dict(zip(graph, count()))
    data = {}
    data['nodes'] = [dict(id=n, **graph.node[n]) for n in graph]
    data['links'] = [dict(source=mapping[u], target=mapping[v]) for u, v in graph.edges()]

    return data
