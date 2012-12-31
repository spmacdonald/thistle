import os
import json
import unittest
from collections import namedtuple

import thistle.apps.build_graph


AppArgs = namedtuple('AppArgs', 'pages_xml, out_json namespace_version')


class TestBuildGraph(unittest.TestCase):
    
    def tearDown(self):
        import os
        os.remove('wikipedia.json')

    def test_app(self):
        pth, _ = os.path.split(os.path.abspath(__file__))
        pages_xml = os.path.join(pth, 'data', 'pages.xml')
        args = AppArgs(pages_xml, 'wikipedia.json', 3)
        thistle.apps.build_graph.main(args)

        with open(os.path.join(pth, 'data', 'wikipedia.json')) as fh:
            expected = json.load(fh)

        with open('wikipedia.json') as fh:
            actual = json.load(fh)

        self.assertEqual(actual, expected)
