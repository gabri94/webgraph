from django.shortcuts import render
from netdiff import OlsrParser, NetJsonParser, diff, BMX6Parser, BatmanParser
import urllib
import json
from webgraph.graph3d.models import Island, Link, Node
import networkx as nx
from django.http import HttpResponse
from networkx.readwrite import json_graph


# Create your views here.


def home(request):
    return HttpResponse("Hello world")


def graph(request, slug):
    # Show the graph of a given island
    context = {'island': slug}
    return render(request, 'graph.html', context)


def graphjs(request, slug):
    island = Island.objects.get(slug=slug)
    parser = NetJsonParser(to_netjson(island=island))
    return HttpResponse(d3_graph(parser.graph))


def update(request, slug):
    # Fetch the data using netdiff and update the db
    # Fetch old_topolog from DB
    # perform diff and update DB

    island = Island.objects.get(slug=slug)
    protocol = island.get_protocol_display()
    graph = ''
    if protocol == 'OLSRv1':
        parser = OlsrParser(island.url)
    elif protocol == 'Batman':
        parser = BatmanParser(island.url)
    elif protocol == 'BMX6':
        parser = BMX6Parser(island.url)
    elif protocol == 'NetJson':
        parser = BMX6Parser(island.url)

    njparser = NetJsonParser(to_netjson(island=island))

    graph_diff = diff(njparser, parser)
    for link in graph_diff['added']:
        node_a, created = Node.objects.get_or_create(address=link[0], island=island)
        node_b, created = Node.objects.get_or_create(address=link[1], island=island)
        if len(link) == 2:
            Link.objects.create(node_a=node_a, node_b=node_b)
        else:
            Link.objects.create(node_a=node_a, node_b=node_b, weight=link[2]['weight'])
    for link in graph_diff['removed']:
        try:
            l = Link.objects.get(node_a__address=link[0], node_b__address=link[1])
            l.delete()
        except DoesNotExist:
            Pass

    return HttpResponse("Done")


def to_netjson(island):
    nodes = []
    links = []
    for node in Node.objects.filter(island__slug=island.slug):
        nodes.append(node.to_netjson())

    for link in Link.objects.filter(node_a__island__slug=island.slug):
        links.append(link.to_netjson())

    NetJson = {'type': 'NetworkGraph',
                'protocol': island.get_protocol_display(),
                'version': '0',
                'metric': '0',
                'router_id': island.url,
                'nodes': nodes,
                'links': links}
    return NetJson


def d3_graph(graph):
    node_bc = nx.betweenness_centrality(graph, weight="weight")
    node_dc = nx.degree_centrality(graph)
    edge_bc = nx.edge_betweenness_centrality(graph, weight="weight")
    nx.set_edge_attributes(graph, 'betweenness', edge_bc)
    for node in graph.nodes():
        graph.node[node]["bw"] = node_bc[node]
        graph.node[node]["dc"] = node_dc[node]
    # print self.new_graph.edges(data=True)
    d3graph = json_graph.node_link_data(graph)
    return json.dumps(d3graph)
