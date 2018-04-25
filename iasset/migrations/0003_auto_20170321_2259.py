# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('iservice', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('iasset', '0002_auto_20170321_2259'),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='storagespace',
            name='create_person',
            field=models.ForeignKey(related_name='storagespace_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='storagespace',
            name='host_on',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u4e3b\u673a', to='iasset.Storage'),
        ),
        migrations.AddField(
            model_name='storagespace',
            name='update_person',
            field=models.ForeignKey(related_name='storagespace_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='storage',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='storage',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='storage',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='server',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='security',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='security',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='security',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='security',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='security',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='rent',
            name='asset',
            field=models.ForeignKey(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='parts',
            name='asset',
            field=models.OneToOneField(related_name='parts_of_asset', to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='parts',
            name='create_person',
            field=models.ForeignKey(related_name='parts_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='parts',
            name='update_person',
            field=models.ForeignKey(related_name='parts_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='others',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='others',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='others',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='others',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='others',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='os',
            name='create_person',
            field=models.ForeignKey(related_name='os_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='os',
            name='update_person',
            field=models.ForeignKey(related_name='os_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='network',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='network',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='idc',
            name='contact',
            field=models.ForeignKey(verbose_name='\u8054\u7cfb\u4eba', blank=True, to='info.Contacts', null=True),
        ),
        migrations.AddField(
            model_name='idc',
            name='contract',
            field=models.ManyToManyField(to='info.Contract', verbose_name='\u5408\u540c'),
        ),
        migrations.AddField(
            model_name='idc',
            name='create_person',
            field=models.ForeignKey(related_name='idc_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='idc',
            name='update_person',
            field=models.ForeignKey(related_name='idc_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='create_person',
            field=models.ForeignKey(related_name='cabinet_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='idc',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u623f', blank=True, to='iasset.IDC', null=True),
        ),
        migrations.AddField(
            model_name='cabinet',
            name='update_person',
            field=models.ForeignKey(related_name='cabinet_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='bladecenter',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='bladecenter',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='bladecenter',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='bladecenter',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='bladecenter',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='blade',
            name='asset',
            field=models.OneToOneField(to='iasset.Asset'),
        ),
        migrations.AddField(
            model_name='blade',
            name='blade_center',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u5200\u7bb1', blank=True, to='iasset.BladeCenter', null=True),
        ),
        migrations.AddField(
            model_name='blade',
            name='cabinet',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True),
        ),
        migrations.AddField(
            model_name='blade',
            name='os_release',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True),
        ),
        migrations.AddField(
            model_name='blade',
            name='service',
            field=models.ForeignKey(verbose_name='\u670d\u52a1\u4fe1\u606f', blank=True, to='iservice.ServiceInfo', null=True),
        ),
        migrations.AddField(
            model_name='blade',
            name='storage_used',
            field=models.ForeignKey(verbose_name='\u5b58\u50a8\u7a7a\u95f4\u4f7f\u7528', blank=True, to='iasset.StorageSpace', null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='contract',
            field=models.ManyToManyField(to='info.Contract', verbose_name='\u5408\u540c'),
        ),
        migrations.AddField(
            model_name='asset',
            name='create_person',
            field=models.ForeignKey(related_name='asset_create_user', verbose_name='\u521b\u5efa\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='asset',
            name='model',
            field=models.ForeignKey(related_name='relatedmodel', verbose_name='\u8bbe\u5907\u578b\u53f7', to='info.ProductModel'),
        ),
        migrations.AddField(
            model_name='asset',
            name='parts',
            field=models.ManyToManyField(related_name='asset_parts', verbose_name='\u914d\u4ef6', to='iasset.Parts'),
        ),
        migrations.AddField(
            model_name='asset',
            name='update_person',
            field=models.ForeignKey(related_name='asset_update_user', verbose_name='\u6700\u540e\u66f4\u65b0\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
