# -*- coding=utf-8 -*-
import logging
import re
import traceback
import urllib2
import headers4spider
from spider_tmall import GoodsDTO


class Spider4innisfree:
    def __init__(self):
        pass

    @staticmethod
    def spider(goods):
        url = goods.g_url

        try:
            goods_id = re.findall('seq=(\d+)', url)[0]
            req = urllib2.Request(url=url, headers=headers4spider.headers_innisfree)
            res = urllib2.urlopen(req).read().decode('utf-8', 'ignore')
        except Exception as e:
            print '无法打开网页:', e.message
            return False

        try:
            title = re.findall('<title>(.*?)</title>', res)
            title = title[0] if title else None
            goods.g_name = title
            # TODO 提取到父类中
            stock_status = re.findall(u'销售中', res)
            if stock_status.__len__() == 0:
                goods.invalid_goods()
                return goods

            line_price = re.findall('price = Number\(\'(.*?)\'\)', res)[0]

            real_price = line_price
            real_stock = 100
            logging.info(u'商品名: {} ; 库存: {} ; 划线价格: {} ; 真实价格: {} ; 商品链接: {}'.format(title, real_stock,
                                                                                     line_price, real_price, url))

        except Exception as e:
            exstr = traceback.format_exc()
            print exstr
            logging.error('数据抽取失败!!! url: %s' % url)
            return False

        goods.g_name = title
        goods.price_lasted = real_price
        goods.stock = real_stock
        return goods


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    url = 'https://www.innisfree.cn/Product.do?method=productView&seq=1000007222'
    goods = GoodsDTO(url)
    Spider4innisfree.spider(goods)
    print goods
