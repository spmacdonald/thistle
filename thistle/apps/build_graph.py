import os
import json

from thistle.graph import DirectedGraph
from thistle.io import WikipediaXmlReader


NAMESPACE = '{{http://www.mediawiki.org/xml/export-0.{0}/}}'


def build_index_map(args):
    index_map = {}

    with open(args.pages_xml) as fh:
        for page in WikipediaXmlReader(fh, NAMESPACE.format(args.namespace_version)):
            if page.redirect or page.special:
                continue

            index_map.setdefault(page.title, {'id': len(index_map), 'text_len': len(page.text)})

    return index_map


def build_graph(args, index_map):
    graph = DirectedGraph()

    with open(args.pages_xml) as fh:
        for page in WikipediaXmlReader(fh, NAMESPACE.format(args.namespace_version)):
            if page.title not in index_map:
                continue

            for link in page.links:
                u = index_map[page.title]['id']
                if link in index_map:
                    graph.add_node(u, title=page.title, text_len=index_map[page.title]['text_len'])
                    v = index_map[link]['id']
                    graph.add_node(v, title=link, text_len=index_map[link]['text_len'])
                    graph.add_edge(u, v)

    return graph


def node_link_data(graph):

    data = {}
    data['nodes'] = [dict(**graph.node[n]) for n in graph]
    data['links'] = [dict(source=graph.node[u]['title'], target=graph.node[v]['title']) for u, v in graph.edges()]

    return data


def main(args):

    print 'Building index map'
    index_map = build_index_map(args)

    print 'Building graph'
    graph = build_graph(args, index_map)
    for n, d in graph.node.iteritems():
        fname = os.path.join(args.out_dir, d['title'])
        with open(fname, 'w') as fh:
            json.dump(node_link_data(graph.extract_edges(n)), fh)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--pages-xml', action='store', required=True)
    parser.add_argument('--out-dir', action='store', required=True)
    parser.add_argument('--namespace-version', action='store', required=True)

    main(parser.parse_args())
