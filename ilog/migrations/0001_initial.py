# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eventtype', models.CharField(max_length=64, verbose_name='\u4e8b\u4ef6\u7c7b\u578b', choices=[(b'add', '\u589e\u52a0'), (b'delete', '\u5220\u9664'), (b'change', '\u66f4\u6539'), (b'login', '\u767b\u5f55')])),
                ('target', models.CharField(max_length=128, verbose_name='\u64cd\u4f5c\u5bf9\u8c61')),
                ('remote_ip', models.CharField(max_length=100, null=True, verbose_name='\u767b\u5f55IP', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u65e5\u671f')),
                ('detail', models.TextField(verbose_name='\u4e8b\u4ef6\u8be6\u60c5')),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6\u65e5\u5fd7',
                'verbose_name_plural': '\u4e8b\u4ef6\u65e5\u5fd7',
            },
        ),
    ]
