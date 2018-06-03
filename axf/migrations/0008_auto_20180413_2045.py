# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-13 12:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0007_cartmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoodsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('og_num', models.IntegerField(default=1)),
                ('og_goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_num', models.CharField(max_length=32)),
                ('o_status', models.IntegerField(default=0)),
                ('o_create_time', models.DateTimeField(auto_now=True)),
                ('o_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.UserModel')),
            ],
        ),
        migrations.AddField(
            model_name='ordergoodsmodel',
            name='og_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='axf.OrderModel'),
        ),
    ]