#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('inetwork.views',
    url(r'^ip/$', 'network_ip', name='network_ip'),
    url(r'^ip/list$', 'network_ip_list', name='network_ip_list'),
    url(r'^ip/add$', 'network_ip_add', name='network_ip_add'),
    url(r'^ip/edit$', 'network_ip_edit', name='network_ip_edit'),
    url(r'^ip/delete$', 'network_ip_delete', name='network_ip_delete'),
    url(r'^segment/$', 'network_segment', name='network_segment'),
    url(r'^segment/list$', 'network_segment_list', name='network_segment_list'),
    url(r'^segment/add$', 'network_segment_add', name='network_segment_add'),
    url(r'^segment/edit$', 'network_segment_edit', name='network_segment_edit'),
    url(r'^segment/delete$', 'network_segment_delete', name='network_segment_delete'),
    url(r'^link/$', 'network_link', name='network_link'),
    url(r'^link/list$', 'network_link_list', name='network_link_list'),
    url(r'^link/add$', 'network_link_add', name='network_link_add'),
    url(r'^link/edit$', 'network_link_edit', name='network_link_edit'),
    url(r'^link/delete$', 'network_link_delete', name='network_link_delete'),
    url(r'^topology/$', 'network_topology', name='network_topology'),
)