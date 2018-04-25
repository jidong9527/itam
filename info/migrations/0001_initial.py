# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u516c\u53f8\u540d\u79f0')),
                ('address', models.CharField(max_length=256, null=True, verbose_name='\u516c\u53f8\u5730\u5740', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u4f9b\u5e94\u5546/\u5382\u5546',
                'verbose_name_plural': '\u4f9b\u5e94\u5546/\u5382\u5546',
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u59d3\u540d')),
                ('phone_number', models.CharField(max_length=30, null=True, verbose_name='\u7535\u8bdd', blank=True)),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='\u90ae\u7bb1', blank=True)),
                ('position', models.CharField(max_length=64, null=True, verbose_name='\u804c\u4f4d', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u8054\u7cfb\u4eba',
                'verbose_name_plural': '\u8054\u7cfb\u4eba',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u5408\u540c\u540d\u79f0')),
                ('sn', models.CharField(max_length=128, null=True, verbose_name='\u5408\u540c\u7f16\u53f7', blank=True)),
                ('cost', models.FloatField(null=True, verbose_name='\u8d39\u7528', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('pdf', models.FileField(upload_to=b'contract/', null=True, verbose_name='\u7535\u5b50\u7248\u5408\u540c', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c',
                'verbose_name_plural': '\u5408\u540c',
            },
        ),
        migrations.CreateModel(
            name='DeviceOfContract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u4e2a\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('ram', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('price', models.FloatField(null=True, verbose_name='\u4ef7\u683c', blank=True)),
                ('quantity', models.IntegerField(null=True, verbose_name='\u8bbe\u5907\u6570\u91cf', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5408\u540c\u91c7\u8d2d\u7684\u8bbe\u5907',
                'verbose_name_plural': '\u5408\u540c\u91c7\u8d2d\u7684\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256, verbose_name='\u8bbe\u5907\u578b\u53f7')),
                ('height', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u9ad8\u5ea6', blank=True)),
                ('asset_type', models.CharField(default=b'server', max_length=64, verbose_name='\u8bbe\u5907\u7c7b\u578b', choices=[(b'server', '\u670d\u52a1\u5668'), (b'bladecenter', '\u5200\u7bb1'), (b'blade', '\u5200\u7247'), (b'vm', '\u865a\u62df\u673a'), (b'network', '\u7f51\u7edc\u8bbe\u5907'), (b'storage', '\u5b58\u50a8\u8bbe\u5907'), (b'tape', '\u5e26\u5e93'), (b'security', '\u5b89\u5168\u8bbe\u5907'), (b'parts', '\u914d\u4ef6'), (b'others', '\u5176\u5b83\u7c7b')])),
                ('power', models.IntegerField(null=True, verbose_name='\u8bbe\u5907\u529f\u7387(W)', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u8bbe\u5907\u578b\u53f7',
                'verbose_name_plural': '\u8bbe\u5907\u578b\u53f7',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u9879\u76ee\u540d\u79f0')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
    ]
