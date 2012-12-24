import unittest

from thistle.graph import DirectedGraph, adjacency_data, adjacency_graph


class TestDirectedGraph(unittest.TestCase):

    def setUp(self):
        g = DirectedGraph()
        edges = [(1, 0), (2, 0), (3, 1), (4, 1), (5, 2), (6, 1), (7, 0), (8, 0), (9, 8)]
        for u, v in edges:
            g.add_node(u, title=u)
            g.add_node(v, title=v)
            g.add_edge(u, v)

        self.g = g

    def test_add_node(self):
        g = DirectedGraph()
        g.add_node(0, title='foo', text_length=10)
        self.assertEqual(g[0], {'text_length': 10, 'title': 'foo'})

    def test_add_edge(self):
        g = DirectedGraph()
        g.add_edge(0, 1)
        g.add_edge(0, 1)
        g.add_edge(1, 1)
        g.add_edge(2, 0)
        self.assertEqual(g.predecessors(0), [2])
        self.assertEqual(g.predecessors(1), [0])

    def test_iter(self):
        self.assertEqual(list(self.g), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_predecessors(self):
        self.assertEqual(self.g.predecessors(0), [1, 2, 7, 8])
        self.assertEqual(self.g.predecessors(1), [3, 4, 6])
        self.assertEqual(self.g.predecessors(2), [5])
        self.assertEqual(self.g.predecessors(3), [])
        self.assertEqual(self.g.predecessors(8), [9])


class TestReadWriteGraph(unittest.TestCase):

    def setUp(self):
        g = DirectedGraph()
        edges = [(0, 3), (0, 4), (0, 5), (0, 6),
                 (1, 8), (2, 8), (2, 1), (2, 4),
                 (2, 6), (2, 0), (3, 1), (3, 2),
                 (3, 6), (3, 7), (3, 8), (3, 9),
                 (4, 3), (6, 1), (6, 9), (7, 0),
                 (7, 1), (7, 2), (7, 4), (7, 5),
                 (7, 6), (8, 1), (8, 2), (9, 8),
                 (9, 2), (9, 4)]
        for u, v in edges:
            g.add_node(u, title=u)
            g.add_node(v, title=v)
            g.add_edge(u, v)

        self.g = g

    def test_adjacency_data(self):
        expected = {'adjacency': [[3L, 4L, 5L, 6L],
                                  [8L],
                                  [8L, 1L, 4L, 6L, 0L],
                                  [1L, 2L, 6L, 7L, 8L, 9L],
                                  [3L],
                                  [],
                                  [1L, 9L],
                                  [0L, 1L, 2L, 4L, 5L, 6L],
                                  [1L, 2L],
                                  [8L, 2L, 4L]],
                    'nodes': [{'id': 0, 'title': 0},
                              {'id': 1, 'title': 1},
                              {'id': 2, 'title': 2},
                              {'id': 3, 'title': 3},
                              {'id': 4, 'title': 4},
                              {'id': 5, 'title': 5},
                              {'id': 6, 'title': 6},
                              {'id': 7, 'title': 7},
                              {'id': 8, 'title': 8},
                              {'id': 9, 'title': 9}]}

        actual = adjacency_data(self.g)
        self.assertEqual(actual, expected)

    def test_adjacency_graph(self):
        data = adjacency_data(self.g)
        graph = adjacency_graph(data)
        self.assertEqual(graph, self.g)
