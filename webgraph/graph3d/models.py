from django.db import models
from django.template.defaultfilters import slugify


ROUTING_PROTOCOL =
{
    'Batman': 1,
    'OLSRv1': 2,
    'BMX': 3
}


class Link(models.Model):
    weight = models.IntegerField(verbose_name=_("link's weight"))
    node_a = models.ForeignKey(Node, verbose_name=_('from node'))
    node_b = models.ForeignKey(Node, verbose_name=_('from node'))
    centrality = models.FloatField()


class Node(models.Model):
    name = models.CharField()
    centrality = models.FloatField()
    address = models.CharField(unique=True)


class Island(models.Model):
    name = models.CharField()
    slug = models.SlugField(max_length=75, db_index=True, unique=True, blank=True)
    proto = choicify(ROUTING_PROTOCOL)
    url = charField()

    def save(self, *args, **kwargs):

        # auto generate slug
        if not self.slug:
            self.slug = slugify(self.name)
