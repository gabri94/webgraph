from django.shortcuts import render

import netdiff.olsr1.Olsr1Parser
# Create your views here.


def viewgraph(request):
    # Show the graph
    return


def update(request):
    # Fetch the data using netdiff and update the db
    # Fetch old_topolog from DB
    # old_top=Link.getall
    firenze = "http://10.150.25.1:9090/"
    response = urllib.urlopen(firenze).read()
    topology = json.loads(response)
    parser = Olsr1Parser(old=Null, new=topology)
    diff = parser.diff(Cost=True)
    Link.add(diff[added])
