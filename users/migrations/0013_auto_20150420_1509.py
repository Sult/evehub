# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0012_remove_membership_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('wallet', models.IntegerField(default=1000000)),
                ('category', models.IntegerField(default=0, choices=[(0, b'User'), (1, b'Corporation'), (2, b'Alliance'), (3, b'Coalition')])),
                ('subscription', models.IntegerField(default=0, choices=[(0, b'Free'), (1, b'Bronze'), (2, b'Silver'), (3, b'Gold')])),
                ('start_date', models.DateField(null=True)),
                ('name', models.CharField(max_length=254, unique=True, null=True)),
                ('key', models.BigIntegerField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='user',
        ),
        migrations.AlterField(
            model_name='leadership',
            name='account',
            field=models.ForeignKey(to='users.Subscription'),
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]
