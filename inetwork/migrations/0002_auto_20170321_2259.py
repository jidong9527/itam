# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0001_initial'),
        ('iasset', '0003_auto_20170321_2259'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0001_initial'),
        ('inetwork', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='segment',
            name='create_person',
            field=models.ForeignKey(related_name='segment_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='segment',
            name='update_person',
            field=models.ForeignKey(related_name='segment_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ports',
            name='connection',
            field=models.ForeignKey(related_name='connect_to', verbose_name='\u8fde\u63a5\u5230', blank=True, to='inetwork.Ports', null=True),
        ),
        migrations.AddField(
            model_name='ports',
            name='create_person',
            field=models.ForeignKey(related_name='ports_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ports',
            name='host',
            field=models.ForeignKey(verbose_name='\u5360\u7528\u8bbe\u5907', to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='ports',
            name='ip',
            field=models.ForeignKey(verbose_name='IP\u5730\u5740', blank=True, to='inetwork.IPAddress', null=True),
        ),
        migrations.AddField(
            model_name='ports',
            name='update_person',
            field=models.ForeignKey(related_name='ports_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='contract',
            field=models.ForeignKey(verbose_name='\u5408\u540c', blank=True, to='info.Contract', null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='create_person',
            field=models.ForeignKey(related_name='link_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='from_idc',
            field=models.ForeignKey(related_name='from_idc', verbose_name='\u4ece\u54ea\u4e2aIDC', blank=True, to='iasset.IDC', null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='to_idc',
            field=models.ForeignKey(related_name='to_idc', verbose_name='\u5230\u54ea\u4e2aIDC', blank=True, to='iasset.IDC', null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='update_person',
            field=models.ForeignKey(related_name='link_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='create_person',
            field=models.ForeignKey(related_name='ip_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='segment',
            field=models.ForeignKey(to='inetwork.Segment'),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='ipaddress',
            name='update_person',
            field=models.ForeignKey(related_name='ip_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='segment',
            unique_together=set([('address', 'mask')]),
        ),
        migrations.AlterUniqueTogether(
            name='ports',
            unique_together=set([('host', 'port_num')]),
        ),
    ]
