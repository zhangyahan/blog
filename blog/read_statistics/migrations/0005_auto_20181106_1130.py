# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-06 11:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0004_auto_20181106_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readdate',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 11, 6, 11, 30, 54, 226666)),
        ),
    ]
