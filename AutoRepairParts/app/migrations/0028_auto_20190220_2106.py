# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-20 16:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20190218_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
