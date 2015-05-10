# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0002_graph_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph',
            name='rrdSourceFilename',
        ),
        migrations.AddField(
            model_name='graph',
            name='rrdFilename',
            field=models.FileField(default='aaaa', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='graph',
            name='end',
            field=models.CharField(default='now', max_length=50),
        ),
        migrations.AlterField(
            model_name='graph',
            name='height',
            field=models.IntegerField(default='180'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='lowerLimit',
            field=models.IntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='lowerLimitRigid',
            field=models.BooleanField(default='true'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='start',
            field=models.CharField(default='end-3600', max_length=50),
        ),
        migrations.AlterField(
            model_name='graph',
            name='verticalLabel',
            field=models.CharField(default='verticalLabel', max_length=50),
        ),
        migrations.AlterField(
            model_name='graph',
            name='watermark',
            field=models.CharField(default='watermark', max_length=50),
        ),
        migrations.AlterField(
            model_name='graph',
            name='width',
            field=models.IntegerField(default='640'),
        ),
    ]
