# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iasset', '0003_auto_20170321_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blade',
            old_name='blade_center',
            new_name='bladecenter',
        ),
    ]
