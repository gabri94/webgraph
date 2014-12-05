from django.contrib import admin
from webgraph.graph3d.models import Island, Node, Link

# Register your models here.

admin.site.register(Island)
admin.site.register(Link)
admin.site.register(Node)
