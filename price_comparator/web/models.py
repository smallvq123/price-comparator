# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# 商品表
class Goods(models.Model):
    id = models.AutoField(primary_key=True)  #
    g_url = models.CharField(max_length=2048, verbose_name=('商品链接'))  #
    g_from_choices = (
        (1, "淘宝"),
        (2, "天猫"),
        (3, "其他（暂未支持）"),
    )
    g_from = models.IntegerField(choices=g_from_choices, default=1, verbose_name=('商品来源'))  #  1，taobao
    g_name = models.CharField(max_length=256, verbose_name=('名称'), null=True, blank=True, default='')  # 商品名称
    price_lasted = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=('最新官网价'), null=True, blank=True)  # 商品最新价格
    price_moniter = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=('监控价格'), null=True, blank=True)  # 监控价格 当最新价格不一致时 needs_update变成true
    needs_update = models.BooleanField(verbose_name=('是否需要更新'), default=False)  # 是否需要更新
    stock = models.IntegerField('库存', null=True, default=-1)  # 库存剩余
    status_choices = (
        (-2, "下架"),
        (-1, "停止更新"),
        (1, "正常更新"),
    )
    status = models.IntegerField(choices=status_choices, default=1, verbose_name=('监控状态'))
    date_created = models.DateTimeField('date created', auto_now_add=True, null=True)
    date_updated = models.DateTimeField('date updated', auto_now=True, null=True)
    category = models.CharField('分类', max_length=256, null=True, blank=True)

    def invalid_goods(self):
        self.needs_update = True
        self.price_lasted = -1
        self.stock = -1
        self.status = -2

    def __str__(self):
        return '{0.g_name}({0.g_url})'.format(self)