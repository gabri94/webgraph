from django.db import models

# Create your models here.


class Link(models.Model):
    weight = models.IntegerField(verbose_name=_("link's weight"))
    node_a = models.ForeignKey(Node, verbose_name=_('from node'))
    node_b = models.ForeignKey(Node, verbose_name=_('from node'))
    centrality = models.FloatField()


class Node(models.Model):
    name = models.CharField()
    centrality = models.FloatField()
    address = models.CharField(unique=True)
