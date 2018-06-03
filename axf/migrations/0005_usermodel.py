# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-09 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0004_goods'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=64)),
                ('icon', models.ImageField(upload_to='icons')),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
    ]
