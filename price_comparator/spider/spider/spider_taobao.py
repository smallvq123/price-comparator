# -*- coding=utf-8 -*-
import logging
import re
import traceback
import urllib2
import headers4spider


class Spider4taobao:
    def __init__(self):
        pass

    @staticmethod
    def spider(goods):
        url = goods.g_url

        goods_id = re.findall('id=(\d+)', url)[0]

        try:
            req = urllib2.Request(url=url, headers=headers4spider.header_taobao)
            res = urllib2.urlopen(req).read().decode('gbk', 'ignore')
        except Exception as e:
            print '无法打开网页:', e.reason
            return False

        try:
            title = re.findall('<h3 class="tb-main-title" data-title="(.*?)"', res)
            title = title[0] if title else None
            goods.g_name = title
            # TODO 提取到父类中
            stock_status = re.findall(u'下架', res)
            if stock_status.__len__() != 0:
                goods.invalid_goods()
                return goods

            line_price = re.findall('<em class="tb-rmb-num">(.*?)</em>', res)[0]

            # 30-42行为抓取淘宝商品真实价格，该数据是动态加载的
            purl = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId={}&modules=dynStock,price,xmpPromotion".format(
                goods_id)

            price_req = urllib2.Request(url=purl, headers=headers4spider.header_taobao)
            price_res = urllib2.urlopen(price_req).read()
            real_price = re.findall('"price":"(.*?)"', price_res)
            real_price = real_price[real_price.__len__() - 1].split(' - ', 1)[0] if real_price else None
            real_stock = re.findall('"stock":(\d+)\w*', price_res)
            real_stock = real_stock[0] if real_stock else None
            logging.info(u'商品名: {} ; 库存: {} ; 划线价格: {} ; 真实价格: {} ; 商品链接: {}'.format(title, real_stock,
                                                                                     line_price, real_price, url))
            # 45-53行为抓取评论数据，该数据也是动态加载的
            # comment_url = "https://rate.tmall.com/list_detail_rate.htm?itemId={}&sellerId=880734502&currentPage=1".format(
            #     goods_id)
            # comment_data = urllib2.urlopen(comment_url).read().decode("GBK", "ignore")
            # temp_data = re.findall('("commentTime":.*?),"days"', comment_data)
            # temp_data = temp_data if temp_data else re.findall('("rateContent":.*?),"reply"', comment_data)
            # comment = ""
            # for data in temp_data:
            #     comment += data.encode('utf-8')
            # comment = comment if comment else "暂无评论"
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
    url = 'https://detail.tmall.com/item.htm?spm=a1z10.5-b-s.w4011-15049790928.121.30b84146vAnkPs&id=520235734978&rn=64a370163d102d156f1281acf6fc8224&abbucket=15'
    # url = raw_input("请输入商品链接: ")
    # spider_taobao(url)
    response = '{"code":{"code":0,"message":"SUCCESS"},"data":{"viewer":{"admin":false,"bs":"","buyDomain":"buy.taobao.com","buyerId":"","cartDomain":"cart.taobao.com","cc":false,"countryCode":"CN","ctUser":false,"lgin":false,"serviceTab":"ITEM","tkn":"e4e56e58d65ee"},"deliveryFee":{"data":{"areaId":110100,"areaName":"\u5317\u4EAC","sendCity":"\u5E7F\u4E1C\u6C55\u5934","serviceInfo":{"list":[{"id":"100_-4","info":"\u5FEB\u9012 <span class=\"wl-yen\">&yen;<\/span>10.00","isDefault":true},{"id":"100_-7","info":"EMS <span class=\"wl-yen\">&yen;<\/span>20.00"}]}},"dataUrl":"\/\/detailskip.taobao.com\/json\/deliveryFee.htm","message":"ok","success":true},"activity":{},"originalPrice":{"def":{"price":"6.90"}},"price":"6.90","tradeContract":{"pay":[{"icons":["\/\/img.alicdn.com\/tfs\/TB1KTHfQFXXXXbnXFXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1XeDvQFXXXXc5XXXXXXXXXXXX-32-32.png"],"title":"\u8682\u8681\u82B1\u5457","url":"\/\/payservice.alipay.com\/intro\/index.htm?c=hb"},{"icons":["\/\/img.alicdn.com\/tfs\/TB1w6O3QFXXXXX4aXXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1c7HAQFXXXXakXXXXXXXXXXXX-32-32.png"],"title":"\u4FE1\u7528\u5361\u652F\u4ED8","url":"\/\/payservice.alipay.com\/intro\/index.htm?c=xyk"},{"icons":["\/\/img.alicdn.com\/tfs\/TB1dvGWQFXXXXcFaXXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1FdDlQFXXXXa5XpXXXXXXXXXX-32-32.png"],"title":"\u96C6\u5206\u5B9D","url":"\/\/jf.alipay.com"}],"service":[{"desc":"\u5546\u54C1\u5728\u8FD0\u8F93\u9014\u4E2D\u51FA\u73B0\u7834\u635F\u7684\uFF0C\u6D88\u8D39\u8005\u53EF\u5411\u5356\u5BB6\u63D0\u51FA\u8865\u5BC4\u7533\u8BF7\uFF0C\u53EF\u8865\u5BC41\u6B21\uFF0C\u8865\u5BC4\u90AE\u8D39\u7531\u5356\u5BB6\u627F\u62C5","icons":["\/\/img.alicdn.com\/tps\/i1\/TB1skruGpXXXXagXFXXAz6UFXXX-16-16.png",null],"linkType":1,"title":"1\u6B21\u7834\u635F\u8865\u5BC4"},{"desc":"\u6EE1\u8DB37\u5929\u65E0\u7406\u7531\u9000\u6362\u8D27\u7533\u8BF7\u7684\u524D\u63D0\u4E0B\uFF0C\u5305\u90AE\u5546\u54C1\u9700\u8981\u4E70\u5BB6\u627F\u62C5\u9000\u8D27\u90AE\u8D39\uFF0C\u975E\u5305\u90AE\u5546\u54C1\u9700\u8981\u4E70\u5BB6\u627F\u62C5\u53D1\u8D27\u548C\u9000\u8D27\u90AE\u8D39\u3002","icons":["\/\/img.alicdn.com\/tps\/i1\/T1EQA5FpVgXXceOP_X-16-16.jpg",null],"linkType":1,"title":"7\u5929\u65E0\u7406\u7531"}]},"dynStock":{"holdQuantity":0,"sellableQuantity":744,"stock":744,"stockType":"normal"},"qrcodeImgUrl":"\/\/gcodex.alicdn.com\/qrcode.do?biz_code=xcode&short_name=a.ZRs8&cmd=createSub&param=id:563661869008;scm:20140619.pc_detail.itemId.0","couponActivity":{"buyerHasMianxi":false,"coupon":{},"shopProm":[{"icon":["\/\/img.alicdn.com\/tfs\/TB1Kz8VQFXXXXa6XFXXXXXXXXXX-56-16.png","\/\/img.alicdn.com\/tfs\/TB1CDp8QFXXXXakXpXXXXXXXXXX-112-32.png"],"title":"\u6EE1150,\u4EAB\u90E8\u5206\u5730\u533A\u5305\u90AE"}],"showMianxiTips":false},"soldQuantity":{"confirmGoodsCount":"2085","soldTotalCount":"2660"},"promotion":{"promoData":{},"saleDetailMap":{}}}})'
    res = 'onSibRequestSuccess({"code":{"code":0,"message":"SUCCESS"},"data":{"viewer":{"admin":false,"bs":"","buyDomain":"buy.taobao.com","buyerId":"","cartDomain":"cart.taobao.com","cc":false,"countryCode":"CN","ctUser":false,"lgin":false,"serviceTab":"ITEM","tkn":"e4e56e58d65ee"},"deliveryFee":{"data":{"areaId":110100,"areaName":"\u5317\u4EAC","sendCity":"\u5E7F\u4E1C\u4F5B\u5C71","serviceInfo":{"list":[{"id":"100_-4","info":"\u5FEB\u9012 \u514D\u8FD0\u8D39","isDefault":true,"markInfo":"24\u5C0F\u65F6\u5185\u53D1\u8D27"}]}},"dataUrl":"\/\/detailskip.taobao.com\/json\/deliveryFee.htm","message":"ok","success":true},"originalPrice":{";1627207:14360222;122216343:3376466;":{"price":"179.00"},";1627207:14360222;122216343:917;":{"price":"179.00"},"def":{"price":"179.00"},";1627207:14360222;122216343:50792021;":{"price":"179.00"},";1627207:14360222;122216343:3285954;":{"price":"179.00"},";1627207:14360222;122216343:568;":{"price":"179.00"}},"upp":{"-2":"\u6DD8\u91D1\u5E01\u6700\u9AD8\u53EF\u62B5\u5546\u54C1\u4EF7<em clas><strong>199<\/strong>\u6DD8\u91D1\u5E01<\/em><em class> \u62B5\uFFE51.99<\/em> <em cl":[{"icons":["\/\/img.alicdn.com\/tfs\/TB1KTHfQFXXXXbnXFXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1XeDvQFXXXXc5XXXXXXXXXXXX-32-32.png"],"title":"\u8682\u8681\u82B1\u5457","url":"\/\/payservice.alipay.com\/intro\/index.htm?c=hb"},{"icons":["\/\/img.alicdn.com\/tfs\/TB1w6O3QFXXXXX4aXXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1c7HAQFXXXXakXXXXXXXXXXXX-32-32.png"],"title":"\u4FE1\u7528\u5361\u652F\u4ED8","url":"\/\/payservice.alipay.com\/intro\/index.htm?c=xyk"},{"icons":["\/\/img.alicdn.com\/tfs\/TB1dvGWQFXXXXcFaXXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1FdDlQFXXXXa5XpXXXXXXXXXX-32-32.png"],"title":"\u96C6\u5206\u5B9D","url":"\/\/jf.alipay.com"}],"service":[{"desc":"\u4FDD\u9669\u516C\u53F8\u5168\u7A0B\u62C5\u4FDD\u8D54\u4ED8\u8BE5\u5546\u54C1\u6BCF\u7B14\u4EA4\u6613\u7684\u552E\u540E","icons":["\/\/gtms04.alicdn.com\/tps\/i4\/TB14MJXLVXXXXaraXXXAz6UFXXX-16-16.png",null],"linkType":1,"title":"\u8BA2\u5355\u9669"},{"desc":"\u6EE1\u8DB37\u5929\u65E0\u7406\u7531\u9000\u6362\u8D27\u7533\u8BF7\u7684\u524D\u63D0\u4E0B\uFF0C\u5305\u90AE\u5546\u54C1\u9700\u8981\u4E70\u5BB6\u627F\u62C5\u9000\u8D27\u90AE\u8D39\uFF0C\u975E\u5305\u90AE\u5546\u54C1\u9700\u8981\u4E70\u5BB6\u627F\u62C5\u53D1\u8D27\u548C\u9000\u8D27\u90AE\u8D39\u3002","icons":["\/\/img.alicdn.com\/tps\/i1\/T1EQA5FpVgXXceOP_X-16-16.jpg",null],"linkType":1,"title":"7\u5929\u65E0\u7406\u7531"},{"icons":["\/\/img.alicdn.com\/tfs\/TB1XMnjQFXXXXXYXFXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB1oOuTQFXXXXazapXXXXXXXXXX-32-32.png"],"linkType":2,"title":"\u8FD0\u8D39\u9669","url":"\/\/ju.mmstat.com\/?url=http:\/\/www.taobao.com\/go\/act\/baoxian\/yunfeixian.php?jlogid=p161456457c0a0"},{"desc":"\u8D2D\u4E70\u8BE5\u5546\u54C1\uFF0C\u6BCF\u7B14\u6210\u4EA4\u90FD\u4F1A\u6709\u76F8\u5E94\u91D1\u989D\u6350\u8D60\u7ED9\u516C\u76CA\u3002\u611F\u8C22\u60A8\u7684\u652F\u6301\uFF0C\u613F\u516C\u76CA\u7684\u5FEB\u4E50\u4F34\u968F\u60A8\u6BCF\u4E00\u5929\u3002","icons":["\/\/img.alicdn.com\/tfs\/TB1wj5PQFXXXXX8apXXXXXXXXXX-16-16.png","\/\/img.alicdn.com\/tfs\/TB13FrcQFXXXXaKXVXXXXXXXXXX-32-32.png"],"linkType":2,"title":"\u516C\u76CA\u5B9D\u8D1D","url":"\/\/service.taobao.com\/support\/knowledge-1117985.htm?spm=0.0.0.0.bOwpfZ&dkey=searchview"}]},"dynStock":{"holdQuantity":0,"sellableQuantity":2499,"sku":{";1627207:14360222;122216343:3376466;":{"holdQuantity":0,"oversold":false,"sellableQuantity":500,"stock":500},";1627207:14360222;122216343:917;":{"holdQuantity":0,"oversold":false,"sellableQuantity":500,"stock":500},";1627207:14360222;122216343:50792021;":{"holdQuantity":0,"oversold":false,"sellableQuantity":500,"stock":500},";1627207:14360222;122216343:3285954;":{"holdQuantity":0,"oversold":false,"sellableQuantity":500,"stock":500},";1627207:14360222;122216343:568;":{"holdQuantity":0,"oversold":false,"sellableQuantity":499,"stock":499}},"stock":2499,"stockType":"normal"},"qrcodeImgUrl":"\/\/gcodex.alicdn.com\/qrcode.do?biz_code=xcode&short_name=a.ZRs8&cmd=createSub&param=id:576700654210;scm:20140619.pc_detail.itemId.0","couponActivity":{"buyerHasMianxi":false,"coupon":{},"showMianxiTips":false},"promotion":{"promoData":{";1627207:14360222;122216343:3376466;":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}],";1627207:14360222;122216343:917;":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}],"def":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}],";1627207:14360222;122216343:50792021;":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}],";1627207:14360222;122216343:3285954;":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}],";1627207:14360222;122216343:568;":[{"cart":true,"loginPromotion":false,"price":"99.90","start":false,"type":"\u65B0\u54C1\u4E0A\u65B0"}]},"saleDetailMap":{}},"soldQuantity":{"confirmGoodsCount":"0","soldTotalCount":"1"}}}); '
    # real_price = re.findall('"price":"(.*?)"', res)[0]
    real_stock = re.findall('"stock":(\d+)\w*', res)
    price_str = '16.90 - 18.90'
    price_str1 = price_str.split(' - ', 1)[0]
    print price_str1
