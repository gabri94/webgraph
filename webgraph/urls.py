from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^$', 'webgraph.views.home', name='home'),
    url(r'^graph/(?P<slug>[-\w]+)/$', 'webgraph.graph3d.views.graph', name='view_graph'),
    url(r'^update/(?P<slug>[-\w]+)/$', 'webgraph.graph3d.views.update', name='update_graph'),
    url(r'^api/graph/(?P<slug>[-\w]+)/$', 'webgraph.graph3d.views.graphjs', name='get_graph_js'))
