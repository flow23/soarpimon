# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('graphs', '0006_auto_20150504_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='lastChange',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 4, 15, 30, 4, 345948, tzinfo=utc), verbose_name='last change', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='graph',
            name='generationDate',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date generated'),
        ),
    ]
