# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-20 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20190220_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=200),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='balance',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='color',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='grandTotal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='labourTotal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='miles',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='model',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='motor',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='paid',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='partTotal',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='plate',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='year',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='part',
            name='part_no',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
