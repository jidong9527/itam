#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('ilog.views',
    url(r'^list/$', 'log_list', name='log_list'),
)