import json

from thistle.graph import DirectedGraph, adjacency_data
from thistle.io import WikipediaXmlReader


NAMESPACE = '{http://www.mediawiki.org/xml/export-0.3/}'


def build_index_map(fname):
    """Maps wikipedia page titles to integers."""

    index_map = {}

    for page in WikipediaXmlReader(open(fname), NAMESPACE):
        if page.redirect or page.special:
            continue

        index_map.setdefault(page.title, len(index_map))

    return index_map


def build_graph(fname, index_map):

    graph = DirectedGraph()

    for page in WikipediaXmlReader(open(fname), NAMESPACE):
        if page.redirect or page.special:
            continue

        for link in page.links:
            u = index_map[page.title]
            graph.add_node(u, title=page.title)
            if link in index_map:
                v = index_map[link]
                graph.add_node(v, title=link)
                graph.add_edge(u, v)

    return graph


def main(args):

    print 'Building index map'
    index_map = build_index_map(args.pages_xml)

    print 'Building graph'
    graph = build_graph(args.pages_xml, index_map)

    print 'Writing graph'
    data = adjacency_data(graph)
    with open('wikipedia.json', 'w') as fh:
        json.dump(data, fh)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pages-xml', action='store', required=True)

    main(parser.parse_args())
