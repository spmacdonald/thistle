import os
import json
import unittest
from collections import namedtuple

import thistle.apps.build_graph


AppArgs = namedtuple('AppArgs', 'pages_xml, out_dir namespace_version')


class TestBuildGraph(unittest.TestCase):
    
    def setUp(self):
        self.out_dir = '.data'
        os.mkdir(self.out_dir)

    def tearDown(self):
        for fname in os.listdir(self.out_dir):
            os.unlink(os.path.join(self.out_dir, fname))

        os.rmdir(self.out_dir)

    def test_app(self):
        pth, _ = os.path.split(os.path.abspath(__file__))
        pages_xml = os.path.join(pth, 'data', 'pages.xml')
        args = AppArgs(pages_xml, self.out_dir, 3)
        thistle.apps.build_graph.main(args)

        self.assertEqual(len(os.listdir(self.out_dir)), 444)

        actual = {u'nodes': [{u'text_len': 26203, u'title': u'Aarhus'},
                             {u'text_len': 10171, u'title': u'Mouthwash'}],
                  u'links': [{u'source': u'Mouthwash', u'target': u'Aarhus'}]}

        expected = json.load(open(os.path.join(self.out_dir, 'Mouthwash')))

        self.assertEqual(actual, expected)
