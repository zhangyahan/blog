# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-04 11:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='博客标题')),
                ('content', models.TextField(verbose_name='博客内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='发布时间')),
                ('last_update_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '博客',
                'db_table': 'blog',
                'verbose_name_plural': '博客',
            },
        ),
        migrations.CreateModel(
            name='BlogTypeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog_type', models.CharField(max_length=32, verbose_name='博客类型')),
            ],
            options={
                'verbose_name': '博客类型',
                'db_table': 'blog_type',
                'verbose_name_plural': '博客类型',
            },
        ),
        migrations.AddField(
            model_name='blogmodel',
            name='blog_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog_index.BlogTypeModel', verbose_name='博客分类'),
        ),
    ]
