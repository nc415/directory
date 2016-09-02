# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-02 12:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0025_person_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='user',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
