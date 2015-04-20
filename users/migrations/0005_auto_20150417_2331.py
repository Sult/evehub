# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20150417_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='membership',
            field=models.IntegerField(default=1, choices=[(1, b'Bronze'), (2, b'Silver'), (3, b'Gold')]),
        ),
    ]
