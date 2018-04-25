# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istatistic', '0001_initial'),
        ('iuser', '0001_initial'),
        ('iservice', '0002_auto_20170321_2259'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecost',
            name='department',
            field=models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe9\x83\xa8\xe9\x97\xa8', to='iuser.Departments'),
        ),
        migrations.AddField(
            model_name='servicecost',
            name='service_name',
            field=models.ForeignKey(verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0', to='iservice.ServiceInfo'),
        ),
        migrations.AddField(
            model_name='departmentcost',
            name='department_name',
            field=models.ForeignKey(verbose_name=b'\xe9\x83\xa8\xe9\x97\xa8\xe5\x90\x8d\xe7\xa7\xb0', to='iuser.Departments'),
        ),
    ]
