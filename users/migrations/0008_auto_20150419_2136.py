# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_profile_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='tags',
            new_name='interests',
        ),
    ]
