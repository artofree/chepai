# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=127, blank=True)),
                ('sourceip', models.CharField(max_length=127, blank=True)),
                ('identity', models.CharField(max_length=127, blank=True)),
                ('url', models.CharField(max_length=127)),
                ('code', models.CharField(max_length=127, blank=True)),
                ('mounth', models.CharField(max_length=127, blank=True)),
            ],
        ),
    ]
