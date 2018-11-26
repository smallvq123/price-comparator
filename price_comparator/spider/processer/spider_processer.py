# -*- coding=utf-8 -*-
import decimal
import logging
import random
import time
import traceback

import spider_settings
from spider_settings import AbstractSpider


class Processer:

    def __needs_update(self, goods):
        if goods.stock < spider_settings.STOCK_LIMIT:
            goods.needs_update = True
        elif (goods.price_moniter == None):
            goods.needs_update = True
        else:
            # 价格差异更新阈值 TODO
            if abs(decimal.Decimal(str(goods.price_lasted)) - decimal.Decimal(
                    str(goods.price_moniter))) > spider_settings.PRICE_DIFFERENCE_LIMIT:
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
            except Exception as e:
                exstr = traceback.format_exc()
                print exstr
                error_count += 1

            # 随机睡 1~10s TODO 提取工具类
            random_sleep_sec = random.randint(spider_settings.SPIDE_SLEEP_TIME_MIN, spider_settings.SPIDE_SLEEP_TIME_MAX)
            time.sleep(random_sleep_sec)
            logging.info('error:{}  ;  success:{} ; '.format(error_count, goods_count))
