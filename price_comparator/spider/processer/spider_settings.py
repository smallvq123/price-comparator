# -*- coding=utf-8 -*-
from ..spider import spider_etude
from ..spider import spider_innisfree
from ..spider import spider_taobao, spider_tmall

SPIDER_DICT = {1: spider_taobao.Spider4taobao.spider,
               2: spider_tmall.Spider4tmall.spider,
               3: spider_innisfree.Spider4innisfree.spider,
               4: spider_etude.Spider4etude.spider}


# 爬虫抽象基类 根据g_from 决定使用哪个方法
class AbstractSpider():
    @staticmethod
    def getSpider(g_from):
        # TODO 不存在抛异常
        return SPIDER_DICT[g_from]


# 库存提醒阈值
STOCK_LIMIT = 20
# 价格变动超过多少进行提醒
PRICE_DIFFERENCE_LIMIT = 1.00
# 每次爬取间隔时间(s)
SPIDE_SLEEP_TIME_MIN=3
SPIDE_SLEEP_TIME_MAX=15
