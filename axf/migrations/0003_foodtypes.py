# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-04-04 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0002_mainshow'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeid', models.CharField(max_length=10)),
                ('typename', models.CharField(max_length=20)),
                ('typesort', models.IntegerField()),
                ('childtypenames', models.CharField(max_length=150)),
            ],
        ),
    ]
