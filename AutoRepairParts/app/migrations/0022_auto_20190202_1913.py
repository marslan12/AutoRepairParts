# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-02 14:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_auto_20190131_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
