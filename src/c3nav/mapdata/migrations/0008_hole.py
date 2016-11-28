# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 22:05
from __future__ import unicode_literals

import c3nav.mapdata.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0007_auto_20161128_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(unique=True, verbose_name='Name')),
                ('geometry', c3nav.mapdata.fields.GeometryField()),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holes', to='mapdata.Level', verbose_name='level')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holes', to='mapdata.Package', verbose_name='map package')),
            ],
            options={
                'default_related_name': 'holes',
                'verbose_name': 'Hole',
                'verbose_name_plural': 'Holes',
            },
        ),
    ]
