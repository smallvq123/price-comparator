# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# 商品表
class Goods(models.Model):
    id = models.AutoField(primary_key=True) #
    g_url = models.CharField(max_length=2048) #
    g_from = models.IntegerField() # 商品类型 1，taobao   TODO enum
    g_name = models.CharField(max_length=256) # 商品名称
    price_lasted = models.DecimalField(max_digits=10, decimal_places=2) # 商品最新价格
    price_moniter = models.DecimalField(max_digits=10, decimal_places=2) # 监控价格 当最新价格不一致时 needs_update变成true
    needs_update = models.BooleanField() # 是否需要更新
    stock = models.IntegerField() # 库存剩余
    status = models.IntegerField() # 商品状态 ： -1，停止更新；1，正常更新；
    date_created = models.DateTimeField('date created', auto_now_add=True)
    date_updated = models.DateTimeField('date updated', auto_now=True)
    category = models.CharField('分类',max_length=256)