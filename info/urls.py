#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.conf.urls import patterns, include, url

urlpatterns = patterns('info.views',
    url(r'^contacts/$', 'contacts', name='contacts'),
    url(r'^contract/$', 'contract', name='contract'),
    url(r'^project/$', 'project', name='project'),
    url(r'^company/$', 'company', name='company'),
    url(r'^company/add$', 'company_add', name='company_add'),
    url(r'^manage/models$', 'manage_models', name='manage_models'),
    url(r'^manage/models/list', 'manage_models_list', name='manage_models_list'),
    url(r'^manage/models/add$', 'manage_models_add', name='manage_models_add'),
    url(r'^manage/models/edit$', 'manage_models_edit', name='manage_models_edit'),
    url(r'^manage/models/del$', 'manage_models_del', name='manage_models_del'),
    url(r'^manage/models/detail$', 'manage_models_detail', name='manage_models_detail'),
)