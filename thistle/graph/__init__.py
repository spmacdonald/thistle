# Follows NetworkX closely.  Stripped down for speed and specialized for my
# application.

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
        # Do not allow loops.
        if u == v:
            return

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

    def predecessors(self, n):
        return list(self.pred[n])

    def successors(self, n):
        return list(self.succ[n])


def adjacency_data(graph):

    data = {}
    data['nodes'] = []
    data['adjacency'] = []

    for n in graph.succ:
        data['nodes'].append(dict(id=n, **graph.node[n]))
        data['adjacency'].append(graph.successors(n))

    return data


def adjacency_graph(data):

    graph = DirectedGraph()

    mapping = []
    for d in data['nodes']:
        n_id = d.pop('id')
        mapping.append(n_id)
        graph.add_node(n_id, **d)

    for i, d in enumerate(data['adjacency']):
        source = mapping[i]
        for target in d:
            graph.add_edge(source, target)

    return graph
