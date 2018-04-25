#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('iuser.views',
    url(r'^user/$', 'user', name='user'),
    url(r'^user/list/$', 'user_list', name='user_list'),
    url(r'^user/add/$', 'user_add', name='user_add'),
    url(r'^user/edit/$', 'user_edit', name='user_edit'),
    url(r'^user/delete/$', 'user_delete', name='user_delete'),
    url(r'^group/$', 'group', name='group'),
    url(r'^group/list/$', 'group_list', name='group_list'),
    url(r'^group/add/$', 'group_add', name='group_add'),
    url(r'^group/edit/$', 'group_edit', name='group_edit'),
    url(r'^group/delete/$', 'group_delete', name='group_delete'),
    url(r'^departments/$', 'departments', name='departments'),
    url(r'^departments/list/$', 'departments_list', name='departments_list'),
    url(r'^departments/add/$', 'departments_add', name='departments_add'),
    url(r'^departments/edit/$', 'departments_edit', name='departments_edit'),
    url(r'^departments/delete/$', 'departments_delete', name='departments_delete'),
)