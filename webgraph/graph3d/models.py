from django.db import models
from django.template.defaultfilters import slugify
# from .utils import choicify

ROUTING_PROTOCOL = {
    'Batman': 1,
    'OLSRv1': 2,
    'BMX': 3
}


class Island(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=75, db_index=True, unique=True)
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


class Link(models.Model):
    weight = models.IntegerField(blank=True)
    node_a = models.ForeignKey(Node, related_name='source node')
    node_b = models.ForeignKey(Node, related_name='dest node')
    centrality = models.FloatField(null=True)

    def to_interop(self, island, python=True):
        if python:
            return {'source': self.node_a.address,
                    'next': self.node_b.address,
                    'cost': self.weight}
