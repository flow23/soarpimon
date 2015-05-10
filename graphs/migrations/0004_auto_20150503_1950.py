# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0003_auto_20150503_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='rrdFilename',
            field=models.FileField(upload_to='media/rrd/'),
        ),
    ]
