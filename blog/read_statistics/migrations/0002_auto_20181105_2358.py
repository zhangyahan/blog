# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-05 23:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read_statistics', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogreadmodel',
            options={'verbose_name': '阅读量', 'verbose_name_plural': '阅读量'},
        ),
        migrations.AlterModelTable(
            name='blogreadmodel',
            table='blog_read',
        ),
    ]
