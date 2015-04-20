# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20150419_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='interests',
            new_name='tags',
        ),
    ]
