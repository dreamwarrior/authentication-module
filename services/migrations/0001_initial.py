# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-28 04:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appID', models.CharField(max_length=255)),
                ('serviceID', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(null=True)),
                ('createdAT', models.DateTimeField(auto_now_add=True)),
                ('updatedAT', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'service_list',
                'ordering': ['appID', 'serviceID'],
                'default_permissions': [],
            },
        ),
        migrations.AlterUniqueTogether(
            name='servicelist',
            unique_together=set([('appID', 'serviceID')]),
        ),
    ]
