# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='description',
            field=models.CharField(default='description', max_length=100),
        ),
    ]
