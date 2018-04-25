# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipaddress', models.GenericIPAddressField(unique=True, verbose_name='IP')),
                ('status', models.CharField(default=b'unuse', max_length=64, verbose_name='\u5360\u7528\u72b6\u6001', choices=[(b'inuse', '\u5360\u7528'), (b'unuse', '\u672a\u5360\u7528')])),
                ('user', models.CharField(max_length=128, null=True, verbose_name='\u5360\u7528\u4eba', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': 'IP\u5730\u5740',
                'verbose_name_plural': 'IP\u5730\u5740',
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='\u94fe\u8def\u540d\u79f0')),
                ('isp', models.CharField(max_length=128, verbose_name='ISP')),
                ('bandwidth', models.CharField(max_length=64, verbose_name='\u5e26\u5bbd')),
                ('link_type', models.CharField(default=b'private', max_length=64, verbose_name='\u94fe\u8def\u7c7b\u578b', choices=[(b'private', '\u4e13\u7ebf'), (b'share', '\u5171\u4eab\u94fe\u8def')])),
                ('cost', models.FloatField(null=True, verbose_name='\u8d39\u7528', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u94fe\u8def',
                'verbose_name_plural': '\u94fe\u8def',
            },
        ),
        migrations.CreateModel(
            name='Ports',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('port_num', models.CharField(max_length=128, verbose_name='\u7aef\u53e3\u53f7')),
                ('description', models.CharField(max_length=256, null=True, verbose_name='\u7aef\u53e3\u63cf\u8ff0', blank=True)),
                ('rate', models.CharField(max_length=64, null=True, verbose_name='\u7aef\u53e3\u901f\u7387', blank=True)),
                ('port_type', models.CharField(default=b'twisted-pair', choices=[(b'twisted-pair', '\u53cc\u7ede\u7ebf(RJ-45)'), (b'multimode-fibre', '\u591a\u6a21\u5149\u7ea4'), (b'single-fibre', '\u5355\u6a21\u5149\u7ea4'), (b'virtual', '\u865a\u62df\u673a\u7aef\u53e3')], max_length=64, blank=True, null=True, verbose_name='\u7aef\u53e3\u7c7b\u578b')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u7aef\u53e3',
                'verbose_name_plural': '\u7f51\u7edc\u7aef\u53e3',
            },
        ),
        migrations.CreateModel(
            name='Segment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_version', models.CharField(default=b'ipv4', max_length=64, verbose_name='\u7c7b\u578b', choices=[(b'ipv4', b'IPv4'), (b'ipv6', b'IPv6')])),
                ('address', models.GenericIPAddressField(verbose_name='\u7f51\u6bb5\u5730\u5740')),
                ('mask', models.IntegerField(verbose_name='\u63a9\u7801\u957f\u5ea6')),
                ('usage', models.CharField(max_length=256, null=True, verbose_name='\u7528\u9014', blank=True)),
                ('used_num', models.CharField(max_length=128, verbose_name='\u5df2\u4f7f\u7528ip\u6570\u91cf')),
                ('unused_num', models.CharField(max_length=128, verbose_name='\u672a\u4f7f\u7528ip\u6570\u91cf')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u6bb5',
                'verbose_name_plural': '\u7f51\u6bb5',
            },
        ),
    ]
