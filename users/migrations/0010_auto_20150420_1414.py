# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20150420_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='paid_until',
            new_name='start_date',
        ),
        migrations.RenameField(
            model_name='membership',
            old_name='ceo',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='created',
        ),
        migrations.AddField(
            model_name='membership',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='membership',
            name='wallet',
            field=models.IntegerField(default=1000000),
        ),
        migrations.AlterField(
            model_name='membership',
            name='category',
            field=models.IntegerField(choices=[(0, b'User'), (1, b'Corporation'), (2, b'Alliance'), (3, b'Coalition')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='name',
            field=models.CharField(max_length=254, unique=True, null=True),
        ),
    ]
