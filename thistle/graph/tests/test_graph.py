import unittest

from thistle.graph import DirectedGraph, node_link_data


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
        self.assertEqual(g.successors(0), [1])
        self.assertEqual(g.predecessors(1), [0, 1])
        self.assertEqual(g.successors(1), [1])

    def test_iter(self):
        self.assertEqual(list(self.g), [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_predecessors(self):
        self.assertEqual(self.g.predecessors(0), [1, 2, 7, 8])
        self.assertEqual(self.g.predecessors(1), [3, 4, 6])
        self.assertEqual(self.g.predecessors(2), [5])
        self.assertEqual(self.g.predecessors(3), [])
        self.assertEqual(self.g.predecessors(8), [9])

    def test_successors(self):
        self.assertEqual(self.g.successors(0), [])
        self.assertEqual(self.g.successors(1), [0])
        self.assertEqual(self.g.successors(2), [0])
        self.assertEqual(self.g.successors(3), [1])
        self.assertEqual(self.g.successors(8), [0])


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

    def test_node_link_data(self):
        expected = {
            'links': [
                {'source': 0, 'target': 3},
                {'source': 0, 'target': 4},
                {'source': 0, 'target': 5},
                {'source': 0, 'target': 6},
                {'source': 1, 'target': 8},
                {'source': 2, 'target': 8},
                {'source': 2, 'target': 1},
                {'source': 2, 'target': 4},
                {'source': 2, 'target': 6},
                {'source': 2, 'target': 0},
                {'source': 3, 'target': 1},
                {'source': 3, 'target': 2},
                {'source': 3, 'target': 6},
                {'source': 3, 'target': 7},
                {'source': 3, 'target': 8},
                {'source': 3, 'target': 9},
                {'source': 4, 'target': 3},
                {'source': 6, 'target': 1},
                {'source': 6, 'target': 9},
                {'source': 7, 'target': 0},
                {'source': 7, 'target': 1},
                {'source': 7, 'target': 2},
                {'source': 7, 'target': 4},
                {'source': 7, 'target': 5},
                {'source': 7, 'target': 6},
                {'source': 8, 'target': 1},
                {'source': 8, 'target': 2},
                {'source': 9, 'target': 8},
                {'source': 9, 'target': 2},
                {'source': 9, 'target': 4}
            ],
            'nodes': [
                {'id': 0, 'title': 0},
                {'id': 1, 'title': 1},
                {'id': 2, 'title': 2},
                {'id': 3, 'title': 3},
                {'id': 4, 'title': 4},
                {'id': 5, 'title': 5},
                {'id': 6, 'title': 6},
                {'id': 7, 'title': 7},
                {'id': 8, 'title': 8},
                {'id': 9, 'title': 9}
            ]
        }

        actual = node_link_data(self.g)
        self.assertEqual(actual, expected)
