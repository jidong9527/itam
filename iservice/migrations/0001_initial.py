# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u670d\u52a1\u540d\u79f0')),
                ('type', models.CharField(default=b'parent', max_length=64, verbose_name='\u7c7b\u578b', choices=[(b'parent', '\u670d\u52a1\u5927\u7c7b'), (b'child', '\u670d\u52a1\u5c0f\u7c7b'), (b'content', '\u670d\u52a1\u5185\u5bb9')])),
                ('level', models.CharField(default=b'one', max_length=64, verbose_name='\u670d\u52a1\u7b49\u7ea7', choices=[(b'one', '1\u7ea7'), (b'two', '2\u7ea7'), (b'three', '3\u7ea7'), (b'four', '4\u7ea7'), (b'five', '5\u7ea7')])),
                ('status', models.CharField(default=b'online', max_length=64, verbose_name='\u72b6\u6001', choices=[(b'online', '\u5df2\u4e0a\u7ebf'), (b'offline', '\u5df2\u4e0b\u7ebf')])),
                ('contact', models.CharField(max_length=128, null=True, verbose_name='\u8054\u7cfb\u4eba', blank=True)),
                ('online_date', models.DateField(null=True, verbose_name='\u4e0a\u7ebf\u65f6\u95f4', blank=True)),
                ('offline_date', models.DateField(null=True, verbose_name='\u4e0b\u7ebf\u65f6\u95f4', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('contract', models.ManyToManyField(to='info.Contract', verbose_name='\u76f8\u5173\u5408\u540c')),
            ],
            options={
                'verbose_name': '\u670d\u52a1',
                'verbose_name_plural': '\u670d\u52a1',
            },
        ),
    ]
