# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u6807\u9898')),
                ('service_cost', models.FloatField(verbose_name='\u670d\u52a1\u6210\u672c')),
                ('device_used', models.FloatField(verbose_name='\u8bbe\u5907\u5360\u7528(\u53f0)')),
                ('renewal_cost', models.FloatField(verbose_name='\u670d\u52a1\u7eed\u4fdd\u6210\u672c')),
                ('repair_parts_cost', models.FloatField(verbose_name='\u7ef4\u4fee\u53ca\u914d\u4ef6\u652f\u51fa')),
                ('channel_cost', models.FloatField(verbose_name='\u573a\u5730\u4fe1\u9053\u652f\u51fa')),
                ('device_depreciation', models.FloatField(verbose_name='\u8bbe\u5907\u6298\u65e7')),
                ('storage_cost', models.FloatField(verbose_name='\u5b58\u50a8\u670d\u52a1\u6210\u672c')),
                ('node_constructed', models.FloatField(verbose_name='\u8282\u70b9\u5efa\u8bbe\u6210\u672c')),
                ('total_cost', models.FloatField(verbose_name='\u603b\u6210\u672c')),
                ('statistic_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6838\u7b97\u65f6\u95f4')),
                ('createDate', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u6807\u9898')),
                ('service_cost', models.FloatField(verbose_name='\u670d\u52a1\u6210\u672c')),
                ('device_used', models.FloatField(verbose_name='\u8bbe\u5907\u5360\u7528(\u53f0)')),
                ('renewal_cost', models.FloatField(verbose_name='\u670d\u52a1\u7eed\u4fdd\u6210\u672c')),
                ('repair_parts_cost', models.FloatField(verbose_name='\u7ef4\u4fee\u53ca\u914d\u4ef6\u652f\u51fa')),
                ('channel_cost', models.FloatField(verbose_name='\u573a\u5730\u4fe1\u9053\u652f\u51fa')),
                ('device_depreciation', models.FloatField(verbose_name='\u8bbe\u5907\u6298\u65e7')),
                ('storage_cost', models.FloatField(verbose_name='\u5b58\u50a8\u670d\u52a1\u6210\u672c')),
                ('node_constructed', models.FloatField(verbose_name='\u8282\u70b9\u5efa\u8bbe\u6210\u672c')),
                ('total_cost', models.FloatField(verbose_name='\u603b\u6210\u672c')),
                ('statistic_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u6838\u7b97\u65f6\u95f4')),
                ('createDate', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
        ),
    ]
