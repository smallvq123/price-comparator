# -*- coding=utf-8 -*-
import decimal
import logging
import random
import time

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
        if goods.stock < 20:
            goods.needs_update = True
        elif (goods.price_moniter == None):
            goods.needs_update = True
        else:
            # 价格差异更新阈值 TODO
            if decimal.Decimal(str(goods.price_lasted)) - decimal.Decimal(str(goods.price_moniter)) > 1:
                goods.needs_update = True
            else:
                goods.needs_update = False
        goods.save()

    # 处理传入goods对象
    def process(self, goods_list):
        goods_count = 0
        error_count = 0
        for goods in goods_list:
            logging.info('now_goods_id:{}'.format(goods.id))
            try:
                if goods.g_url == None:
                    logging.error('商品url为None goodsid: %s' % str(goods.id))
                    continue
                spider_func = AbstractSpider.getSpider(goods.g_from)
                goods = spider_func(goods)
                if goods:
                    # 判断是否需要更新
                    self.__needs_update(goods)
                    goods_count += 1
                else:
                    error_count += 1
            except:
                error_count += 1
            # 随机睡 1~10s TODO 提取工具类
            random_sleep_sec = random.randint(3, 20)
            time.sleep(random_sleep_sec)
            logging.info('error:{}  ;  success:{} ; '.format(error_count, goods_count))
