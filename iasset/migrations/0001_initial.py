# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_number', models.CharField(max_length=128, null=True, verbose_name='\u8d44\u4ea7\u7f16\u53f7', blank=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u8bbe\u5907\u540d\u79f0')),
                ('sn', models.CharField(max_length=128, verbose_name='\u5e8f\u5217\u53f7')),
                ('purchase_date', models.DateField(null=True, verbose_name='\u8d2d\u4e70\u65f6\u95f4', blank=True)),
                ('warranty_period', models.SmallIntegerField(null=True, verbose_name='\u8d28\u4fdd\u5e74\u9650', blank=True)),
                ('expire_date', models.DateField(null=True, verbose_name='\u8fc7\u4fdd\u65f6\u95f4', blank=True)),
                ('cost', models.FloatField(null=True, verbose_name='\u6210\u672c', blank=True)),
                ('renewal_date', models.DateField(null=True, verbose_name='\u7eed\u4fdd\u65f6\u95f4', blank=True)),
                ('renewal_cost', models.FloatField(null=True, verbose_name='\u7eed\u4fdd\u6210\u672c', blank=True)),
                ('total_cost', models.FloatField(null=True, verbose_name='\u8d44\u4ea7\u603b\u503c', blank=True)),
                ('asset_admin', models.CharField(max_length=64, null=True, verbose_name='\u8bbe\u5907\u7ba1\u7406\u5458', blank=True)),
                ('status', models.CharField(default=b'unuse', max_length=128, verbose_name='\u8bbe\u5907\u72b6\u6001', choices=[(b'purchasing', '\u91c7\u8d2d'), (b'unuse', '\u672a\u7528'), (b'inuse', '\u5728\u7528'), (b'loan', '\u501f\u51fa'), (b'troubling', '\u6545\u969c'), (b'maintaining', '\u7ef4\u4fee'), (b'off', '\u4e0b\u67b6'), (b'abandoned', '\u62a5\u5e9f')])),
                ('online_date', models.DateField(null=True, verbose_name='\u4e0a\u67b6\u65f6\u95f4', blank=True)),
                ('offline_date', models.DateField(null=True, verbose_name='\u4e0b\u67b6\u65f6\u95f4', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u66f4\u65b0\u65f6\u95f4')),
                ('qrcode', models.ImageField(upload_to=b'iasset/qrcode/', null=True, verbose_name='\u4e8c\u7ef4\u7801', blank=True)),
                ('picture', models.ImageField(upload_to=b'iasset/img/', null=True, verbose_name='\u8bbe\u5907\u56fe\u7247', blank=True)),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u8d44\u4ea7\u603b\u8868',
                'verbose_name_plural': '\u8d44\u4ea7\u603b\u8868',
            },
        ),
        migrations.CreateModel(
            name='Blade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('slotNum', models.SmallIntegerField(null=True, verbose_name='\u69fd\u4f4d', blank=True)),
            ],
            options={
                'verbose_name': '\u5200\u7247\u670d\u52a1\u5668',
                'verbose_name_plural': '\u5200\u7247\u670d\u52a1\u5668',
            },
        ),
        migrations.CreateModel(
            name='BladeCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('slotSum', models.SmallIntegerField(null=True, verbose_name='\u69fd\u4f4d\u603b\u6570', blank=True)),
            ],
            options={
                'verbose_name': '\u5200\u7bb1',
                'verbose_name_plural': '\u5200\u7bb1',
            },
        ),
        migrations.CreateModel(
            name='Cabinet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=256, verbose_name='\u673a\u67dc\u540d\u79f0')),
                ('location', models.CharField(max_length=256, null=True, verbose_name='\u4f4d\u7f6e', blank=True)),
                ('layer', models.IntegerField(default=42, verbose_name='\u603b\u5c42\u6570')),
                ('specifications', models.CharField(max_length=128, null=True, verbose_name='\u89c4\u683c', blank=True)),
                ('status', models.CharField(default=b'available', max_length=16, verbose_name='\u72b6\u6001', choices=[(b'available', '\u53ef\u7528'), (b'unavailable', '\u4e0d\u53ef\u7528')])),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u673a\u67dc',
                'verbose_name_plural': '\u673a\u67dc',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name='\u673a\u623f\u540d\u79f0')),
                ('address', models.TextField(null=True, verbose_name='\u5730\u5740', blank=True)),
                ('status', models.CharField(default=b'available', max_length=16, verbose_name='\u72b6\u6001', choices=[(b'available', '\u53ef\u7528'), (b'unavailable', '\u4e0d\u53ef\u7528')])),
                ('isself', models.CharField(default=b'self', max_length=16, verbose_name='\u81ea\u5efa/\u79df\u501f', choices=[(b'self', '\u81ea\u6709'), (b'lease', '\u79df\u501f')])),
                ('cost', models.FloatField(null=True, verbose_name='\u6210\u672c(\u5143)', blank=True)),
                ('start_date', models.DateField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='\u7ed3\u675f\u65f6\u95f4', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u673a\u623f',
                'verbose_name_plural': '\u673a\u623f',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
            ],
            options={
                'verbose_name': '\u7f51\u7edc\u8bbe\u5907',
                'verbose_name_plural': '\u7f51\u7edc\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(unique=True, max_length=128, verbose_name='\u7248\u672c')),
                ('os_type', models.CharField(default=b'linux', max_length=64, verbose_name='\u7cfb\u7edf\u7c7b\u578b', choices=[(b'linux', b'Linux'), (b'unix', b'unix'), (b'windows', b'Windows')])),
                ('soft_license', models.CharField(max_length=256, null=True, verbose_name='\u8bb8\u53ef\u8bc1', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u64cd\u4f5c\u7cfb\u7edf',
                'verbose_name_plural': '\u64cd\u4f5c\u7cfb\u7edf',
            },
        ),
        migrations.CreateModel(
            name='Others',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
            ],
            options={
                'verbose_name': '\u5176\u5b83\u8bbe\u5907',
                'verbose_name_plural': '\u5176\u5b83\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parts_type', models.CharField(max_length=32, choices=[(b'nic', '\u7f51\u5361'), (b'cpu', '\u5904\u7406\u5668'), (b'memory', '\u5185\u5b58\u6761'), (b'disk', '\u786c\u76d8'), (b'camera', '\u6444\u50cf\u5934'), (b'others', '\u5176\u4ed6')])),
                ('unit_price', models.FloatField(null=True, verbose_name='\u5355\u4ef7', blank=True)),
                ('used', models.IntegerField(null=True, verbose_name='\u5df2\u7528', blank=True)),
                ('rest', models.IntegerField(null=True, verbose_name='\u5269\u4f59', blank=True)),
                ('specifications', models.CharField(max_length=128, null=True, verbose_name='\u89c4\u683c', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u914d\u4ef6',
                'verbose_name_plural': '\u914d\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_or_to', models.CharField(default=b'to', max_length=64, verbose_name='\u79df\u7528/\u501f\u51fa', choices=[(b'from', '\u79df\u7528'), (b'to', '\u501f\u51fa')])),
                ('receiver', models.CharField(max_length=64, null=True, verbose_name='\u63a5\u624b\u4eba', blank=True)),
                ('receiver_phone', models.CharField(max_length=64, null=True, verbose_name='\u63a5\u624b\u4eba\u8054\u7cfb\u65b9\u5f0f', blank=True)),
                ('receiver_company', models.CharField(max_length=128, null=True, verbose_name='\u63a5\u624b\u4eba\u5355\u4f4d', blank=True)),
                ('handler', models.CharField(max_length=64, null=True, verbose_name='\u7ecf\u529e\u4eba', blank=True)),
                ('handler_phone', models.CharField(max_length=64, null=True, verbose_name='\u7ecf\u529e\u4eba\u8054\u7cfb\u65b9\u5f0f', blank=True)),
                ('handler_company', models.CharField(max_length=128, null=True, verbose_name='\u7ecf\u529e\u4eba\u5355\u4f4d', blank=True)),
                ('rent_date', models.DateField(null=True, verbose_name='\u8d77\u59cb\u65f6\u95f4', blank=True)),
                ('rent_period', models.SmallIntegerField(null=True, verbose_name='\u79df\u671f', blank=True)),
                ('returned_date', models.DateField(null=True, verbose_name='\u5f52\u8fd8\u65e5\u671f', blank=True)),
                ('returned_status', models.CharField(default=b'notreturned', max_length=64, verbose_name='\u5f52\u8fd8/\u672a\u5f52\u8fd8', choices=[(b'returned', '\u5f52\u8fd8'), (b'notreturned', '\u672a\u5f52\u8fd8')])),
                ('usage', models.CharField(max_length=256, null=True, verbose_name='\u7528\u9014', blank=True)),
                ('rent_cost', models.FloatField(null=True, verbose_name='\u79df\u501f\u6210\u672c', blank=True)),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Security',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
            ],
            options={
                'verbose_name': '\u5b89\u5168\u8bbe\u5907',
                'verbose_name_plural': '\u5b89\u5168\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('total_storage', models.FloatField(null=True, verbose_name='\u5b58\u50a8\u603b\u91cf(G)', blank=True)),
            ],
            options={
                'verbose_name': '\u5b58\u50a8\u8bbe\u5907',
                'verbose_name_plural': '\u5b58\u50a8\u8bbe\u5907',
            },
        ),
        migrations.CreateModel(
            name='StorageSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='\u540d\u79f0')),
                ('volume', models.IntegerField(verbose_name='\u7a7a\u95f4\u5bb9\u91cf(G)')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u66f4\u65b0\u65f6\u95f4')),
                ('memo', models.TextField(null=True, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'verbose_name': '\u5b58\u50a8\u7a7a\u95f4',
                'verbose_name_plural': '\u5b58\u50a8\u7a7a\u95f4',
            },
        ),
        migrations.CreateModel(
            name='Tape',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('total', models.IntegerField(null=True, verbose_name='\u78c1\u5e26\u603b\u91cf(\u76d8)', blank=True)),
                ('used', models.IntegerField(null=True, verbose_name='\u5df2\u7528(\u76d8)', blank=True)),
                ('specification', models.CharField(max_length=128, null=True, verbose_name='\u78c1\u5e26\u89c4\u683c', blank=True)),
            ],
            options={
                'verbose_name': '\u78c1\u5e26\u5e93',
                'verbose_name_plural': '\u78c1\u5e26\u5e93',
            },
        ),
        migrations.CreateModel(
            name='VM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.SmallIntegerField(null=True, verbose_name='\u8bbe\u5907\u4f4d\u7f6e', blank=True)),
                ('raid_type', models.CharField(max_length=512, null=True, verbose_name='raid\u7c7b\u578b', blank=True)),
                ('cpu_count', models.SmallIntegerField(null=True, verbose_name='CPU\u6838\u6570', blank=True)),
                ('cpu_model', models.CharField(max_length=128, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('memory', models.FloatField(null=True, verbose_name='\u5185\u5b58\u5927\u5c0f(G)', blank=True)),
                ('disk', models.FloatField(null=True, verbose_name='\u78c1\u76d8\u5bb9\u91cf(G)', blank=True)),
                ('asset', models.OneToOneField(to='iasset.Asset')),
                ('cabinet', models.ForeignKey(verbose_name='\u6240\u5728\u673a\u67dc', blank=True, to='iasset.Cabinet', null=True)),
                ('host', models.ForeignKey(related_name='vm_host', verbose_name='\u5bbf\u4e3b\u673a', to='iasset.Asset')),
                ('os_release', models.ForeignKey(verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7248\u672c', blank=True, to='iasset.OS', null=True)),
            ],
            options={
                'verbose_name': '\u865a\u62df\u673a',
                'verbose_name_plural': '\u865a\u62df\u673a',
            },
        ),
    ]
