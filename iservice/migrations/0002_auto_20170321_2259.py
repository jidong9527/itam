# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinfo',
            name='create_person',
            field=models.ForeignKey(related_name='serviceinfo_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='serviceinfo',
            name='department',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u90e8\u95e8', blank=True, to='iuser.Departments', null=True),
        ),
        migrations.AddField(
            model_name='serviceinfo',
            name='parent_service',
            field=models.ForeignKey(related_name='parent_level', verbose_name='\u7236\u7ea7\u670d\u52a1', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='serviceinfo',
            name='update_person',
            field=models.ForeignKey(related_name='serviceinfo_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
    ]
