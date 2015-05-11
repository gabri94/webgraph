from django.db import models
from django.template.defaultfilters import slugify
# from .utils import choicify

ROUTING_PROTOCOL = {
    'Batman': 1,
    'OLSRv1': 2,
    'BMX6': 3,
    'NetJson': 4
}


def choicify(dictionary):
    """
    Converts a readable python dictionary into a django model/form
    choice structure (list of tuples) ordered based on the values of each key

    :param dictionary: the dictionary to convert
    """
    # get order of the fields
    ordered_fields = sorted(dictionary, key=dictionary.get)
    choices = []
    # loop over each field
    for field in ordered_fields:
        # build tuple (value, i18n_key)
        row = (dictionary[field], field.replace('_', ' '))
        # append tuple to choices
        choices.append(row)
    # return django sorted choices
    return choices


class Island(models.Model):
    protocol = models.IntegerField(choices=choicify(ROUTING_PROTOCOL))
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=75, db_index=True, unique=True, blank=True)
    # proto = choicify(ROUTING_PROTOCOL)
    url = models.CharField(max_length=128)

    def save(self, *args, **kwargs):

        # auto generate slug
        if not self.slug:
            self.slug = slugify(self.name)
        super(Island, self).save(*args, **kwargs)


class Node(models.Model):
    name = models.CharField(blank=True, max_length=128)
    centrality = models.FloatField(null=True)
    address = models.CharField(max_length=128, unique=True)
    island = models.ForeignKey(Island)

    def to_netjson(self):
        return {'id': self.address,
                'label': self.name}


class Link(models.Model):
    weight = models.FloatField(default=1.0)
    node_a = models.ForeignKey(Node, related_name='source node')
    node_b = models.ForeignKey(Node, related_name='dest node')
    centrality = models.FloatField(null=True)

    def to_netjson(self, python=True):
        if python:
            return {'source': self.node_a.address,
                    'target': self.node_b.address,
                    'weight': self.weight}

    def add_link(self, tupla, island):
        node_a, created = Node.objects.get_or_create(address=tupla[0], island=island)
        node_b, created = Node.objects.get_or_create(address=tupla[1], island=island)
        Link.objects.create(node_a=node_a, node_b=node_b, weight=tupla[2]['weight'])
