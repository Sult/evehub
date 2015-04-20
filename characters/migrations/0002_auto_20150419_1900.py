# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='characterapiicon',
            old_name='relation',
            new_name='character',
        ),
        migrations.AlterUniqueTogether(
            name='characterapiicon',
            unique_together=set([('size', 'character')]),
        ),
    ]
