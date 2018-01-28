# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django


class Migration(migrations.Migration):

    if django.VERSION < (1, 8, 0):
        dependencies = [
            ('auth', '__first__'),
        ]
    else:
        dependencies = [
            ('auth', '0006_require_contenttypes_0002'),
        ]
    if django.VERSION < (2, 0, 0):
        operations = [
            migrations.CreateModel(
                name='Background',
                fields=[
                    ('user', models.OneToOneField(related_name='initial_avatars', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                    ('R', models.IntegerField()),
                    ('G', models.IntegerField()),
                    ('B', models.IntegerField()),
                ],
            ),
        ]
    else:
        operations = [
            migrations.CreateModel(
                name='Background',
                fields=[
                    ('user', models.OneToOneField(related_name='initial_avatars', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
                    ('R', models.IntegerField()),
                    ('G', models.IntegerField()),
                    ('B', models.IntegerField()),
                ],
            ),
        ]
