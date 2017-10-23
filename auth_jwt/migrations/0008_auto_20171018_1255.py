# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-18 06:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_jwt', '0007_auto_20171018_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='appID',
        ),
        migrations.AddField(
            model_name='activity',
            name='app',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='user',
            field=models.CharField(max_length=255, null=True),
        ),
    ]