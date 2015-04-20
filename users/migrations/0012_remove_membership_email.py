# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20150420_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='email',
        ),
    ]
