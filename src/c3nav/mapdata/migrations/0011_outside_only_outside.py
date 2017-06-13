# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 11:17
from __future__ import unicode_literals

from django.db import migrations, models


def secondary_level_spaces_inside(apps, schema_editor):
    Space = apps.get_model('mapdata', 'Space')
    Space.objects.filter(section__on_top_of__isnull=False).update(outside=False)



class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0010_on_top_of'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='outside',
            field=models.BooleanField(default=False, verbose_name='only outside of building'),
        ),
        migrations.RunPython(secondary_level_spaces_inside),
    ]