from django.shortcuts import render
from netdiff.olsr1 import Olsr1Parser
import urllib
import json
from webgraph.graph3d.models import Island, Link, Node
from django.http import HttpResponse


# Create your views here.


def home(request):
    return HttpResponse("Hello world")


def graph(request, slug):
    # Show the graph of a given island
    context = {'island': slug}
    return render(request, 'graph.html', context)


def graphjs(request, slug):
    parser = Olsr1Parser(newint=to_interop_list(island=slug))
    island = Island.objects.get(slug=slug)
    return HttpResponse(parser.gen_graph())


def update(request, slug):
    # Fetch the data using netdiff and update the db
    # Fetch old_topolog from DB
    # perform diff and update DB

    island = Island.objects.get(slug=slug)
    response = urllib.urlopen(island.url).read()
    topology = json.loads(response)
    parser = Olsr1Parser(oldint=to_interop_list(island=slug), new=topology)
    diff = parser.diff(cost=0)
    for link in diff['added']:
        node_a, created = Node.objects.get_or_create(address=link[0], island=island)
        node_b, created = Node.objects.get_or_create(address=link[1], island=island)
        Link.objects.create(node_a=node_a, node_b=node_b, weight=link[2]['weight'])
    for link in diff['removed']:
        link.objects.get(node_a=link[0], node_b=link[1]).delete()

    return HttpResponse("Done")


def to_interop_list(island):
    interop = []
    for link in Link.objects.filter(node_a__island__slug=island):
        interop.append(link.to_interop(island=island))
    return {'routes': interop}
