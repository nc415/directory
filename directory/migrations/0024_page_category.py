# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0023_auto_20160902_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='directory.Category'),
        ),
    ]
