# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0005_auto_20150417_2331'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2)),
                ('timezone', models.CharField(blank=True, max_length=3, choices=[(b'USA', b'American'), (b'AUS', b'Australian'), (b'EU', b'European')])),
                ('avatar', models.OneToOneField(null=True, to='characters.CharacterApi')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
