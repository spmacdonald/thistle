# Follows NetworkX closely.  Stripped down for speed and specialized for my
# application.

from array import array
from collections import defaultdict


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
        self.pred = defaultdict(lambda: array('I'))
        self.succ = defaultdict(lambda: array('I'))

    def __eq__(self, other):
        return self.node == other.node and self.pred == other.pred and self.succ == other.succ

    def add_node(self, n, **attr):
        # Will silently overwrite attr if n already exists.
        self.node[n] = attr

    def add_edge(self, u, v):
        # Do not allow loops.
        if u == v:
            return

        if v not in self.succ[u]:
            self.succ[u].append(v)

        if u not in self.pred[v]:
            self.pred[v].append(u)

    def predecessors(self, n):
        return list(self.pred[n])

    def successors(self, n):
        return list(self.succ[n])


def generate_adjlist(graph):
    for s in graph.succ:
        line = '{0} {1}'.format(s, ' '.join(map(str, graph.successors(s))))
        yield line


def write_adjlist(graph, fname):
    with open(fname, 'w') as fh:
        for line in generate_adjlist(graph):
            line += '\n'
            fh.write(line)


def read_adjlist(fname):
    graph = DirectedGraph()

    with open(fname, 'r') as fh:
        for line in fh:
            values = map(int, line.strip().split(' '))
            for v in values[1:]:
                graph.add_edge(values[0], v)

    return graph
