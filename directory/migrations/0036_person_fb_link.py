# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-21 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0035_person_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='FB_link',
            field=models.URLField(blank=True),
        ),
    ]
