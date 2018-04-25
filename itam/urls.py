from django.conf.urls import patterns, include, url
from django.contrib import admin
from itam import settings


urlpatterns = patterns('itam.views',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index', name='index'),
    url(r'^login/$', 'Login', name='login'),
    url(r'^logout/$', 'Logout', name='logout'),
    url(r'^isetting', 'setting', name='setting'),
    url(r'^iasset/', include('iasset.urls')),
    url(r'^ilog/', include('ilog.urls')),
    url(r'^inetwork/', include('inetwork.urls')),
    url(r'^info/', include('info.urls')),
    url(r'^iservice/', include('iservice.urls')),
    url(r'^istatistic/', include('istatistic.urls')),
    url(r'^iuser/', include('iuser.urls')),
)