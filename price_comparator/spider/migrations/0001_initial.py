# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Spider_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('goods_id', models.IntegerField()),
                ('g_url', models.CharField(max_length=2048, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe9\x93\xbe\xe6\x8e\xa5')),
                ('g_from', models.IntegerField(choices=[(1, b'\xe6\xb7\x98\xe5\xae\x9d'), (2, b'\xe5\xa4\xa9\xe7\x8c\xab'), (3, b'\xe5\x85\xb6\xe4\xbb\x96\xef\xbc\x88\xe6\x9a\x82\xe6\x9c\xaa\xe6\x94\xaf\xe6\x8c\x81\xef\xbc\x89')], default=1, verbose_name=b'\xe5\x95\x86\xe5\x93\x81\xe6\x9d\xa5\xe6\xba\x90')),
                ('g_name', models.CharField(blank=True, default=b'', max_length=256, null=True, verbose_name=b'\xe5\x90\x8d\xe7\xa7\xb0')),
                ('price_lasted', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name=b'\xe6\x9c\x80\xe6\x96\xb0\xe5\xae\x98\xe7\xbd\x91\xe4\xbb\xb7')),
                ('stock', models.IntegerField(default=-1, null=True, verbose_name=b'\xe5\xba\x93\xe5\xad\x98')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name=b'date created')),
                ('date_updated', models.DateTimeField(auto_now=True, null=True, verbose_name=b'date updated')),
                ('category', models.CharField(blank=True, max_length=256, null=True, verbose_name=b'\xe5\x88\x86\xe7\xb1\xbb')),
            ],
        ),
    ]