# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20150420_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='category',
            field=models.IntegerField(default=0, choices=[(0, b'User'), (1, b'Corporation'), (2, b'Alliance'), (3, b'Coalition')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='membership',
            name='membership',
            field=models.IntegerField(default=0, choices=[(0, b'Free'), (1, b'Bronze'), (2, b'Silver'), (3, b'Gold')]),
        ),
    ]
