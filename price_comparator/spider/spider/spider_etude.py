# -*- coding=utf-8 -*-
import json
import logging
import re
import time
import traceback
import urllib
import urllib2
import headers4spider
from spider_tmall import GoodsDTO


class Spider4etude:
    @staticmethod
    def spider(goods):
        url = goods.g_url
        goods_id = re.findall('prdCode=(\d+)', url)[0]

        try:
            form_data = {
                'prdCode': goods_id,
            }
            detail_url = 'http://www.etude.cn/app/product/detail.json'
            data = urllib.urlencode(form_data).encode('utf-8')
            req = urllib2.Request(url=detail_url, data=data, headers=headers4spider.headers_etude)
            res = urllib2.urlopen(req).read().decode('utf-8', 'ignore')
        except Exception as e:
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
            return False

        try:
            response_json = json.loads(res)
            product = response_json['data']['product']
            title = product['name']
            goods.g_name = title

            # TODO 移动到父类中
            stock_status = product['status']
            if stock_status != u'L':
                goods.invalid_goods()
                return goods
            line_price = product['standardPrice']
            salePrice = product['salePrice']
            real_price = line_price
            if salePrice > 0.0:
                real_price = salePrice

            real_stock = 100
            logging.info(u'商品名: {} ; 库存: {} ; 划线价格: {} ; 真实价格: {} ; 商品链接: {}'.format(title, real_stock,
                                                                                     line_price, real_price, url))
        except Exception as e:
            exstr = traceback.format_exc()
            print exstr
            logging.error(u'数据抽取失败!!! url: %s' % url)
            return False
        goods.g_name = title
        goods.price_lasted = real_price
        goods.stock = real_stock
        return goods

    def __init__(self):
        pass


#
if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    url = 'http://www.etude.cn/product.html?prdCode=100019638'
    goods = GoodsDTO(url)
    # # url = raw_input("请输入商品链接: ")
    Spider4etude.spider(goods)
    print goods
