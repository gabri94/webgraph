from django.shortcuts import render
import netdiff.olsr1.Olsr1Parser

# Create your views here.


def home(request):

    return


def graph(request, island):
    # Show the graph of a given island
    return


def graphjs(request, island):
    


def update(request, island):
    # Fetch the data using netdiff and update the db
    # Fetch old_topolog from DB
    # old_top=Link.getall
    url = Island.objects.get(slug=island)
    response = urllib.urlopen(url).read()
    topology = json.loads(response)
    parser = Olsr1Parser(new=topology)
    diff = parser.diff(Cost=True)
    Link.add(diff[added])
