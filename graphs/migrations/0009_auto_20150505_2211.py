# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0008_auto_20150505_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='imageFilename',
            field=models.ImageField(upload_to='graph/', blank=True),
        ),
        migrations.AlterField(
            model_name='graph',
            name='rrdFilename',
            field=models.FileField(upload_to='rrd/', blank=True),
        ),
        migrations.AlterField(
            model_name='graph',
            name='timePeriod',
            field=models.IntegerField(default=3600, max_length=10, choices=[('3600', '1hour'), ('43200', '12hours'), ('86400', '1day'), ('604800', '1week'), ('2419200', '1month'), ('14515200', '6months'), ('29030400', '1year')]),
        ),
    ]
