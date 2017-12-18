# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-18 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


def remove_all_tokens(apps, schema_editor):
    apps.get_model('mapdata', 'AccessPermissionToken').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mapdata', '0059_multiple_accesspermissions'),
    ]

    operations = [
        migrations.RunPython(remove_all_tokens, remove_all_tokens),
        migrations.RemoveField(
            model_name='accesspermission',
            name='token',
        ),
        migrations.AddField(
            model_name='accesspermissiontoken',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='accesspermissiontoken',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='accesspermission',
            name='token',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='accesspermissions', to='mapdata.AccessPermissionToken',
                                    verbose_name='Access permission token'),
        ),
    ]
