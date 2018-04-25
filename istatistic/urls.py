#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('istatistic.views',
    url(r'^service/$', 'service', name='service'),
    url(r'^department/$', 'department', name='department'),
    url(r'^project/$', 'porject', name='project'),
)