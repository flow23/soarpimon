# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0004_auto_20150503_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='timePeriod',
            field=models.IntegerField(default='3600'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='rrdFilename',
            field=models.FileField(upload_to='rrd/'),
        ),
    ]
