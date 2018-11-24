# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-17 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20181012_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='g_custom_name',
            field=models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='\u540d\u79f0-\u5b9a\u4e49'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='\u5206\u7c7b'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='g_from',
            field=models.IntegerField(choices=[(1, '\u6dd8\u5b9d'), (2, '\u5929\u732b'), (3, '\u5176\u4ed6\uff08\u6682\u672a\u652f\u6301\uff09')], default=1, verbose_name='\u5546\u54c1\u6765\u6e90'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='g_name',
            field=models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='\u540d\u79f0-\u6293\u53d6'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='needs_update',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u9700\u8981\u66f4\u65b0'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price_lasted',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='\u6700\u65b0\u5b98\u7f51\u4ef7'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='price_moniter',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='\u76d1\u63a7\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='status',
            field=models.IntegerField(choices=[(-2, '\u4e0b\u67b6'), (-1, '\u505c\u6b62\u66f4\u65b0'), (1, '\u6b63\u5e38\u66f4\u65b0')], default=1, verbose_name='\u76d1\u63a7\u72b6\u6001'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='stock',
            field=models.IntegerField(default=-1, null=True, verbose_name='\u5e93\u5b58'),
        ),
    ]
