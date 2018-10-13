# -*- coding=utf-8 -*-
import json
import logging
import re
import time
import traceback
import urllib2


class Spider4tmall:
    @staticmethod
    def spider(goods):
        url = goods.g_url
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.3',
            'Referer': 'https://list.tmall.com/search_product.htm?q=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Connection': 'keep-alive',
        }

        goods_id = re.findall('id=(\d+)', url)[0]
        sku_id = re.findall('skuId=(\d+)', url)[0]
        try:
            req = urllib2.Request(url=url, headers=headers)
            res = urllib2.urlopen(req).read().decode('gbk', 'ignore')
        except Exception as e:
            print '无法打开网页:', e.reason

        try:
            title = re.findall('"title":"(.*?)"', res)
            title = title[0] if title else None
            line_price = re.findall('"reservePrice":"(.*?)"', res)[0]
            t = time.time()
            timestamp = (int(round(t * 1000)))
            # 30-42行为抓取淘宝商品真实价格，该数据是动态加载的
            purl = "https://mdskip.taobao.com/core/initItemDetail.htm?cachedTimestamp={}&itemId={}&callback=setMdskip&timestamp={}".format(
                str(timestamp - 315000), goods_id, timestamp)
            headers_price = {
                'Host': "mdskip.taobao.com",
                "cookie": "miid=1416914392893341000; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; l=ArS04f0dgYQRMtMqetwpb6bSBHkmodh3; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1; cna=5w2/EagEn1sCAbcnVm41KZrQ; t=41a78c0d4f8236cec127e49a3a1d7668; _m_h5_tk=22cd676b46cffe81b7111f72345a4001_1515316266867; _m_h5_tk_enc=594d3f94ed8fe96523affc4889339ae4; enc=LUFqvB76IYLq0NOBSAnqkWEGqx3%2BVDxCaFTpeHTRbd0shSzi6kJ4TKcjRtCKKhB5vGwnjUQpJXJWux06z0QC5w%3D%3D; cookie2=13A91D312332FF9E6F9441B09BD42AEF; v=0; _tb_token_=f385ee7fb8e5b; mt=ci%3D-1_1; isg=BEpKIf4uJNw9j6sTmsbzTbXNmzAsk8-R8Wr4btSFcR3_h-1BvMnkp5C_k_Nbd0Yt",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.2; rv:29.0) Gecko/20100101 Firefox/29.0",
                'Referer': 'http://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.12.UpuePQ&is_b=1&id=' + str(
                    goods_id)}
            price_req = urllib2.Request(url=purl, headers=headers_price)
            price_res = urllib2.urlopen(price_req).read()
            price_res = price_res.decode('UTF-8', 'ignore')
            response_json_reg = '\((.*?)\)'
            response_json_str = re.findall(response_json_reg, price_res)[0]
            response_json = json.loads(response_json_str)
            real_price = response_json['defaultModel']['itemPriceResultDO']['priceInfo'][sku_id]['price']
            real_stock = response_json['defaultModel']['inventoryDO']['skuQuantity'][sku_id]['quantity']

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
