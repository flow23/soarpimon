# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0010_auto_20150506_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='unit',
            field=models.CharField(default='A', max_length=3, choices=[('A', 'Ampere'), ('V', 'Volt'), ('W', 'Wattage')]),
        ),
    ]
