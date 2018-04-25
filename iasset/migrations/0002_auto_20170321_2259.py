# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0001_initial'),
        ('iasset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vm',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='vm',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='tape',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='tape',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='tape',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='tape',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='tape',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
    ]
