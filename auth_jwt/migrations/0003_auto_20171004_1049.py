# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-04 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_jwt', '0002_auto_20170928_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auth',
            name='deviceID',
            field=models.TextField(db_index=True),
        ),
        migrations.AlterField(
            model_name='auth',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
