# -*- coding=utf-8 -*-
from ..spider import spider_taobao, spider_tmall

SPIDER_DICT = {1: spider_taobao.Spider4taobao.spider, 2: spider_tmall.Spider4tmall.spider};


# 爬虫抽象基类 根据g_from 决定使用哪个方法
class AbstractSpider():
    @staticmethod
    def getSpider(g_from):
        # TODO 不存在抛异常
        return SPIDER_DICT[g_from]


class Processer:

    def __needs_update(self, goods):
        if goods.stock < 10:
            goods.needs_update = True
        if goods.price_lasted != goods.price_moniter:
            goods.needs_update = True
        goods.save()

    # 处理传入goods对象
    def process(self, goods_list):

        for goods in goods_list:
            spider_func = AbstractSpider.getSpider(goods.g_from)
            goods = spider_func(goods)
            if goods:
                # 判断是否需要更新
                self.__needs_update(goods)
