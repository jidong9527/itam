# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='create_person',
            field=models.ForeignKey(related_name='project_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='project',
            name='update_person',
            field=models.ForeignKey(related_name='project_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='create_person',
            field=models.ForeignKey(related_name='pm_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='manufactory',
            field=models.ForeignKey(verbose_name='\u5382\u5546', blank=True, to='info.Company', null=True),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='update_person',
            field=models.ForeignKey(related_name='pm_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='deviceofcontract',
            name='contract',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u5408\u540c', to='info.Contract'),
        ),
        migrations.AddField(
            model_name='deviceofcontract',
            name='create_person',
            field=models.ForeignKey(related_name='doc_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='deviceofcontract',
            name='model',
            field=models.ForeignKey(verbose_name='\u8bbe\u5907\u578b\u53f7', to='info.ProductModel'),
        ),
        migrations.AddField(
            model_name='deviceofcontract',
            name='update_person',
            field=models.ForeignKey(related_name='doc_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='contract',
            name='company',
            field=models.ForeignKey(verbose_name='\u4f9b\u5e94\u5546', to='info.Company'),
        ),
        migrations.AddField(
            model_name='contract',
            name='create_person',
            field=models.ForeignKey(related_name='contract_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='contract',
            name='project',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u9879\u76ee', to='info.Project'),
        ),
        migrations.AddField(
            model_name='contract',
            name='update_person',
            field=models.ForeignKey(related_name='contract_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='company',
            field=models.ForeignKey(verbose_name='\u516c\u53f8', to='info.Company'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='create_person',
            field=models.ForeignKey(related_name='contacts_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='contacts',
            name='update_person',
            field=models.ForeignKey(related_name='contacts_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
        migrations.AddField(
            model_name='company',
            name='create_person',
            field=models.ForeignKey(related_name='company_create_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u521b\u5efa\u4eba'),
        ),
        migrations.AddField(
            model_name='company',
            name='update_person',
            field=models.ForeignKey(related_name='company_update_user', default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u6700\u540e\u66f4\u65b0\u4eba'),
        ),
    ]
