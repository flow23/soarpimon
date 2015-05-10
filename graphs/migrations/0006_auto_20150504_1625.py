# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0005_auto_20150503_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='category',
            field=models.CharField(max_length=7, choices=[('solar', 'Solar'), ('battery', 'Battery'), ('wattage', 'Wattage')]),
        ),
    ]
