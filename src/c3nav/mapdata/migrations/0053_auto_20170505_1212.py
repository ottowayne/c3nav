# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 12:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0052_remove_level_intermediate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='escalator',
            name='area',
        ),
        migrations.DeleteModel(
            name='Escalator',
        ),
    ]