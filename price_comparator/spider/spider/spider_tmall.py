# -*- coding=utf-8 -*-
import json
import logging
import re
import time
import traceback
import urllib2
import headers4spider


class Spider4tmall:
    @staticmethod
    def spider(goods):
        url = goods.g_url
        goods_id = re.findall('id=(\d+)', url)[0]

        try:
            req = urllib2.Request(url=url, headers=headers4spider.header_tmall_detail)
            res = urllib2.urlopen(req).read().decode('gbk', 'ignore')
        except Exception as e:
            print '无法打开网页:', e.reason
            return False

        try:
            title = re.findall('"title":"(.*?)"', res)
            title = title[0] if title else None
            goods.g_name = title
            # TODO 移动到父类中
            stock_status = re.findall(u'下架', res)
            if stock_status.__len__() != 0:
                goods.invalid_goods()
                return goods
            line_price = re.findall('"reservePrice":"(.*?)"', res)[0]
            t = time.time()
            timestamp = (int(round(t * 1000)))
            # 30-42行为抓取淘宝商品真实价格，该数据是动态加载的
            # purl = "https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cachedTimestamp={}&itemId={}&callback=setMdskip&timestamp={}".format(
            #     str(timestamp - 315000), goods_id, timestamp)
            purl = "https://mdskip.taobao.com/core/initItemDetail.htm?isUseInventoryCenter=false&cartEnable=true" \
                   "&service3C=false&isApparel=false&isSecKill=false&tmallBuySupport=true&isAreaSell=false" \
                   "&tryBeforeBuy=false&offlineShop=false&itemId={}&showShopProm=false&isPurchaseMallPage=false" \
                   "&isRegionLevel=false&household=false&sellerPreview=false" \
                   "&queryMemberRight=true&addressLevel=2&isForbidBuyItem=false&callback=setMdskip&callback=setMdskip&timestamp={}".format(
                goods_id, timestamp)
            sku_id = re.findall('skuId=(\d+)', url)
            sku_id = sku_id[0] if sku_id else None
            price_req = urllib2.Request(url=purl, headers=headers4spider.headers_price_tmall)
            price_res = urllib2.urlopen(price_req).read()
            price_res = price_res.decode('UTF-8', 'ignore')
            response_json_reg = '\((.*?)\)'
            response_json_str = re.findall(response_json_reg, price_res)[0]
            response_json = json.loads(response_json_str)

            # 是否存在skuid
            if sku_id:
                real_stock = response_json['defaultModel']['inventoryDO']['icTotalQuantity'][sku_id]['quantity']
            else:
                sku_id = 'def'
                real_stock = response_json['defaultModel']['inventoryDO']['icTotalQuantity']

            real_price_promotionList = response_json['defaultModel']['itemPriceResultDO']['priceInfo'][sku_id][
                'promotionList']
            if real_price_promotionList:
                # 登陆后有优惠政策
                real_price = real_price_promotionList[0]['price']
            else:
                real_price = response_json['defaultModel']['itemPriceResultDO']['priceInfo'][sku_id]['price']

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
# if __name__ == '__main__':
#     url = 'https://detail.tmall.com/item.htm?spm=a222t.8750074.6871376497.1.56de14f3UfGY3N&id=578153420589&scene=taobao_shop&skuId=3844563292151'
# # url = raw_input("请输入商品链接: ")
# Spider4tmall.spider_tmall(url)
