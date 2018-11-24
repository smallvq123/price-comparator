# -*- coding: utf-8 -*-
from django.db import models


class Spider_log(models.Model):
    id = models.AutoField(primary_key=True)
    goods_id = models.IntegerField()
    g_url = models.CharField(max_length=2048, verbose_name=('商品链接'))  #
    g_from_choices = (
        (1, "淘宝"),
        (2, "天猫"),
        (3, "悦诗风吟官网"),
        (4, "伊穆之屋（暂未支持）"),
        (-1, "其他（暂未支持）"),
    )
    g_from = models.IntegerField(choices=g_from_choices, default=1, verbose_name=('商品来源'))  # 1，taobao
    g_name = models.CharField(max_length=256, verbose_name=('名称'), null=True, blank=True, default='')  # 商品名称
    price_lasted = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=('最新官网价'), null=True,
                                       blank=True)  # 商品最新价格
    stock = models.IntegerField('库存', null=True, default=-1)  # 库存剩余
    date_created = models.DateTimeField('date created', auto_now_add=True, null=True)
    date_updated = models.DateTimeField('date updated', auto_now=True, null=True)
    category = models.CharField('分类', max_length=256, null=True, blank=True)
