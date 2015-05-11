from django.contrib import admin
from webgraph.graph3d.models import Island, Node, Link

# Register your models here.


class LinkAdmin(admin.ModelAdmin):
    list_display = ('node_a', 'node_b')


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')


class IslandAdmin(admin.ModelAdmin):
    list_display = ('name', 'protocol')


admin.site.register(Island, IslandAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Node, NodeAdmin)
