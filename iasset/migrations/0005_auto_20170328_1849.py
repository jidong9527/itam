# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iasset', '0004_auto_20170328_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='model',
            field=models.ForeignKey(related_name='relatedmodel', verbose_name='\u8bbe\u5907\u578b\u53f7', blank=True, to='info.ProductModel', null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='sn',
            field=models.CharField(max_length=128, null=True, verbose_name='\u5e8f\u5217\u53f7', blank=True),
        ),
    ]
