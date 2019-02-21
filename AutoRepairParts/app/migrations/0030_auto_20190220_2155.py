# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-20 16:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20190220_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='grandTotal',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='labourTotal',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='partTotal',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='part',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Part'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoiceitems',
            name='price',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='part',
            name='price',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='part',
            name='stock',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
    ]
