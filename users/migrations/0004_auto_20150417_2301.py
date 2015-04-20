# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20150416_1255'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.IntegerField(choices=[(0, b'Corporation'), (1, b'Alliance'), (2, b'Coalition')])),
                ('membership', models.IntegerField(default=0, choices=[(0, b'Free'), (1, b'Silver'), (2, b'Gold'), (3, b'Platinum')])),
                ('created', models.DateField(auto_now_add=True)),
                ('paid_until', models.DateField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(unique=True, max_length=254)),
                ('key', models.BigIntegerField(null=True)),
                ('ceo', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='account',
            name='ceo',
        ),
        migrations.AlterField(
            model_name='leadership',
            name='account',
            field=models.ForeignKey(to='users.Membership'),
        ),
        migrations.DeleteModel(
            name='Account',
        ),
    ]
