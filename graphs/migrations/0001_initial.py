# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=1, choices=[('S', 'Solar'), ('B', 'Battery'), ('W', 'Wattage')])),
                ('generationDate', models.DateTimeField(verbose_name='date generated')),
                ('rrdSourceFilename', models.CharField(max_length=50)),
                ('imageFilename', models.ImageField(upload_to='')),
                ('start', models.CharField(max_length=50)),
                ('end', models.CharField(max_length=50)),
                ('verticalLabel', models.CharField(max_length=50)),
                ('watermark', models.CharField(max_length=50)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('upperLimit', models.IntegerField()),
                ('lowerLimit', models.IntegerField()),
                ('lowerLimitRigid', models.BooleanField()),
            ],
        ),
    ]
