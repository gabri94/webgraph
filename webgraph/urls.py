from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns
('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webgraph.views.home', name='home')
    url(r'^graph/(?P<slug>[-\w]+)', 'webgraph.views.graph')
    url(r'^api/graph/(?P<slug>[-\w]+)', 'webgraph.views.graphjs'))
