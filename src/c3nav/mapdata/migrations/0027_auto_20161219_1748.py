# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0026_auto_20161219_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='arealocation',
            name='routing_inclusion',
            field=models.CharField(choices=[('default', 'Default, include if map package is unlocked'), ('allow_exclude', 'Included, but allow excluding'), ('allow_include', 'Excluded, but allow includinge'), ('needs_permission', 'Excluded, needs permission to include')], default='default', max_length=20, verbose_name='Routing Inclusion'),
        ),
        migrations.AddField(
            model_name='locationgroup',
            name='routing_inclusion',
            field=models.CharField(choices=[('default', 'Default, include if map package is unlocked'), ('allow_exclude', 'Included, but allow excluding'), ('allow_include', 'Excluded, but allow includinge'), ('needs_permission', 'Excluded, needs permission to include')], default='default', max_length=20, verbose_name='Routing Inclusion'),
        ),
    ]
