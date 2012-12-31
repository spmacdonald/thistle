import json

from thistle.graph import DirectedGraph, adjacency_data
from thistle.io import WikipediaXmlReader


NAMESPACE = '{{http://www.mediawiki.org/xml/export-0.{0}/}}'


def build_index_map(args):
    """Maps wikipedia page titles to integers."""

    index_map = {}

    with open(args.pages_xml) as fh:
        for page in WikipediaXmlReader(fh, NAMESPACE.format(args.namespace_version)):
            if page.redirect or page.special:
                continue

            index_map.setdefault(page.title, len(index_map))

    return index_map


def build_graph(args, index_map):
    graph = DirectedGraph()

    with open(args.pages_xml) as fh:
        for page in WikipediaXmlReader(fh, NAMESPACE.format(args.namespace_version)):
            if page.redirect or page.special:
                continue

            for link in page.links:
                u = index_map[page.title]
                if link in index_map:
                    graph.add_node(u, title=page.title)
                    v = index_map[link]
                    graph.add_node(v, title=link)
                    graph.add_edge(u, v)

    return graph


def main(args):

    index_map = build_index_map(args)

    graph = build_graph(args, index_map)

    data = adjacency_data(graph)
    with open(args.out_json, 'w') as fh:
        json.dump(data, fh)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pages-xml', action='store', required=True)
    parser.add_argument('--out-json', action='store', required=True)
    parser.add_argument('--namespace-version', action='store', required=True)

    main(parser.parse_args())
