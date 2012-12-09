import os
import unittest

from thistle.io import WikipediaXmlReader


class TestWikipediaXmlReader(unittest.TestCase):

    def setUp(self):
        pth, _ = os.path.split(os.path.abspath(__file__))
        filepath = os.path.join(pth, 'data', 'pages.xml')
        fh = open(filepath)

        namespace = '{http://www.mediawiki.org/xml/export-0.3/}'
        self.reader = WikipediaXmlReader(fh, namespace)

    def test_titles(self):
        titles = [page.title for page in self.reader]

        self.assertEqual(1000, len(titles))

        expected = ['AmericanSamoa',
                    'AppliedEthics',
                    'AccessibleComputing',
                    'Anarchism',
                    'AfghanistanHistory',
                    'AfghanistanGeography',
                    'AfghanistanPeople',
                    'AfghanistanEconomy',
                    'AfghanistanCommunications',
                    'AfghanistanTransportations']

        self.assertEqual(titles[0:10], expected)

    def test_unicode_titles(self):
        titles = [page.title for page in self.reader if type(page.title) == unicode]

        expected = [u'Amhr\xe1n na bhFiann',
                    u'Andr\xe9 Gide',
                    u'Alfonso Cuar\xf3n',
                    u'Casa Batll\xf3',
                    u'Park G\xfcell',
                    u'Casa Mil\xe0',
                    u'Atanasoff\u2013Berry Computer',
                    u'Andr\xe9-Marie Amp\xe8re',
                    u'\xc6esop',
                    u'\xc1lfheimr']

        self.assertEqual(titles, expected)

    def test_categories(self):

        expected = set([u'Acetates',
                        u'Benzoic acids',
                        u'Bayer brands',
                        u'Genericized trademarks',
                        u'Antiplatelet drugs',
                        u'Non-steroidal anti-inflammatory drugs',
                        u'Equine medications',
                        u'Aspirin'])

        actual = [page.categories for page in self.reader if page.title == 'Aspirin'][0]

        self.assertEqual(actual, expected)

    def test_links(self):

        result = {}
        for page in self.reader:
            result[page.title] = page.links

        expected = set(['Fleury', '960', 'Abbo of Fleury', 'monastery',
                        'Villefranche-de-Longchat', 'Jean Mabillon', 'France',
                        'Franks', 'Saint-Germain-des-Pres', 'Monumenta Germaniae Historica',
                        'Georg Waitz', 'twelfth century',
                        '1010', 'Acta Sanctorum', 'Middle Ages', 'abbot'])

        self.assertEqual(result['Aimoin'], expected)
