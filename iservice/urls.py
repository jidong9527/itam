#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('iservice.views',
    url(r'^index/$', 'service_index', name='service_index'),
    url(r'^list/$', 'service_list', name='service_list'),
    url(r'^add/$', 'service_add', name='service_add'),
    url(r'^edit/$', 'service_edit', name='service_edit'),
    url(r'^delete/$', 'service_delete', name='service_delete'),
    # url(r"^add_batch/$", 'service_add_batch', name='service_add_batch'),
)