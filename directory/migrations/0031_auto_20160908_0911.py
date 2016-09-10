# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-08 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0030_auto_20160907_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('slug', 'name', 'user')]),
        ),
    ]
