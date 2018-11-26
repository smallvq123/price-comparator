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
            print 'traceback.format_exc():\n%s' % traceback.format_exc()
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
            response_json_reg = '\((.*?)\)$'
            response_json_str = re.findall(response_json_reg, price_res)[0]
            response_json = json.loads(response_json_str)

            # 是否存在skuid 取真实库存
            if sku_id:
                real_stock = response_json['defaultModel']['inventoryDO']['skuQuantity'][sku_id]['quantity']
            else:
                real_stock = response_json['defaultModel']['inventoryDO']['icTotalQuantity']

            # 取售价 3种情况 有skuid、无、有预售
            price_info = response_json['defaultModel']['itemPriceResultDO']['priceInfo']
            if sku_id:
                real_price = Spider4tmall.get_real_price(price_info, sku_id)
            else:
                for sku_id_dict in price_info:
                    sku_id = sku_id_dict
                    break
                real_price = Spider4tmall.get_real_price(price_info, sku_id)

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

    @staticmethod
    def get_real_price(price_info, sku_id):
        real_price_promotionlist = None
        if 'promotionList' in price_info[sku_id]:
            real_price_promotionlist = price_info[sku_id]['promotionList']
        if 'suggestivePromotionList' in price_info[sku_id]:
            real_price_promotionlist = price_info[sku_id]['suggestivePromotionList']
        try:
            wrt_info = price_info[sku_id]['wrtInfo']
        except:
            wrt_info = None
        if real_price_promotionlist:
            # 登陆后有优惠政策
            real_price = real_price_promotionlist[0]['price']
        else:
            real_price = price_info[sku_id]['price']
        if wrt_info:
            # 存在预售的时候 使用预售价格
            real_price = (wrt_info['finalPayment'] + wrt_info['price']) / 100.00
        return real_price


class GoodsDTO():
    def __init__(self, url):
        self.g_url = url
    g_url = ""
    g_name = ""
    g_custom_name = ""  # 用户自定义名称
    price_lasted = 0.00  # 商品最新价格
    price_moniter = 0.00  # 监控价格 当最新价格不一致时 needs_update变成true
    needs_update = False  # 是否需要更新
    stock = -1  # 库存剩余

    def __str__(self):
        return 'g_name:{}, price_lasted:{}, stock:{}'.format(self.g_name, self.price_lasted, self.stock)


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    url = 'https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14571266849.59.209e48b7JczZWe&id=38666802106&rn=721fbfeb83f7d0bcafd0b4c2f8ed272f&abbucket=2&skuId=4046421802512'
    goods = GoodsDTO(url)
    # # url = raw_input("请输入商品链接: ")
    Spider4tmall.spider(goods)
    print goods
    # json1 = 'setMdskip({"defaultModel":{"bannerDO":{"success":true},"deliveryDO":{"areaId":110101,"deliveryAddress":"日本","deliverySkuMap":{"default":[{"arrivalNextDay":false,"arrivalThisDay":false,"forceMocked":false,"money":"0.00","name":"运费","postageFree":true,"signText":"24:00前付款，10月23日送达，晚到必赔","skuDeliveryAddress":"日本","type":1}],"3220516048299":[{"arrivalNextDay":false,"arrivalThisDay":false,"forceMocked":false,"money":"0.00","name":"运费","postageFree":true,"signText":"24:00前付款，10月23日送达，晚到必赔","skuDeliveryAddress":"日本","type":1}]},"destination":"北京市","expressServiceMap":{"3220516048299":["911"]},"success":true,"tips":{"text":"24:00前付款，10月23日送达，晚到必赔"},"transfername":"菜鸟上海保税1号仓"},"detailPageTipsDO":{"crowdType":0,"hasCoupon":true,"hideIcons":false,"jhs99":false,"minicartSurprise":0,"onlyShowOnePrice":false,"priceDisplayType":4,"primaryPicIcons":[],"prime":false,"showCuntaoIcon":false,"showDou11Style":false,"showDou11SugPromPrice":false,"showDou12CornerIcon":false,"showDuo11Stage":0,"showJuIcon":false,"showMaskedDou11SugPrice":false,"success":true,"trueDuo11Prom":false},"doubleEleven2014":{"doubleElevenItem":false,"halfOffItem":false,"showAtmosphere":false,"showRightRecommendedArea":false,"step":0,"success":true},"extendedData":{},"extras":{},"gatewayDO":{"changeLocationGateway":{"queryDelivery":true,"i_channel":"1110006525315001","queryProm":true},"success":true,"trade":{"addToBuyNow":{},"addToCart":{}}},"internationalComponent":{"consumerProtections":[],"fromName":"日本品牌 菜鸟上海保税1号仓发货","nationalIcon":"//g.alicdn.com/mui/flag-img/circle@2x/JP.png","serviceLogo":"//img.alicdn.com/tps/TB1256qIFXXXXXDXpXXXXXXXXXX.png","shopCertificateIcon":"//img.alicdn.com/tps/TB1db7kKFXXXXcCXVXXXXXXXXXX-171-148.png","success":true,"suppliedByHkBrand":false,"suppliedByHkFair":true,"suppliedByHkOfficialSeller":false,"suppliedByHkOfficialWebsite":false,"suppliedByHkSupermarket":false,"suppliedByHkTaxFreeSeller":false,"tariff":{"name":"进口税","value":"预计14.00元"}},"inventoryDO":{"hidden":false,"icTotalQuantity":100,"skuQuantity":{"3220516048299":{"quantity":100,"totalQuantity":63062,"type":1}},"success":true,"totalQuantity":63062,"type":1},"itemPriceResultDO":{"areaId":110100,"duo11Item":false,"duo11Stage":0,"extraPromShowRealPrice":false,"halfOffItem":false,"hasDPromotion":false,"hasMobileProm":false,"hasTmallappProm":false,"hiddenNonBuyPrice":false,"hideMeal":false,"priceInfo":{"3220516048299":{"areaSold":true,"onlyShowOnePrice":false,"price":"128.00","promotionList":[{"amountPromLimit":0,"amountRestriction":"","basePriceType":"IcPrice","canBuyCouponNum":0,"endTime":1540223999000,"extraPromTextType":0,"extraPromType":0,"limitProm":false,"postageFree":false,"price":"125.00","promType":"normal","start":false,"startTime":1539964800000,"status":2,"tfCartSupport":false,"tmallCartSupport":false,"type":"买遍全球","unLogBrandMember":false,"unLogShopVip":false,"unLogTbvip":false}],"sortOrder":0}},"queryProm":false,"success":true,"successCall":true,"tmallShopProm":[]},"memberRightDO":{"activityType":0,"level":0,"postageFree":false,"shopMember":false,"success":true,"time":0,"value":0.0},"miscDO":{"bucketId":9,"city":"北京","cityId":110100,"debug":{},"hasCoupon":false,"region":"东城区","regionId":110101,"rn":"1087d99e4b1b5ba39e1f08fcb4a1dc26","smartBannerFlag":"top","success":true,"supportCartRecommend":false,"systemTime":"1540041855086","town":"东华门街道","townId":110101001},"regionalizedData":{"success":true},"sellCountDO":{"sellCount":"67","success":true},"servicePromise":{"has3CPromise":false,"servicePromiseList":[{"description":"承诺正品保障，假一赔十","displayText":"正品保障","icon":"//img.alicdn.com/tps/TB1pSTEIFXXXXX7XpXXXXXXXXXX.png","link":"//rule.tmall.hk/gseller/rule/rule_detail.htm?id=1573&tag=self","rank":-1},{"description":"确认收货之日15天(含)内，如有商品质量问题、描述不符或溢漏损失缺发等（不包括因主观原因导致不想要）可申请退货","displayText":"15天售后无忧","icon":"//gw.alicdn.com/tfscom/TB1FWIuQVXXXXcVXXXXXXXXXXXX.png","link":"//rule.tmall.hk/rule/rule_detail.htm?spm=0.0.0.0.td6AIz&id=1519&tag=self","rank":-1},{"description":"进口商品承诺由国内保税区发货","displayText":"进口保税","icon":"//gtms02.alicdn.com/tps/i2/TB1mheXIVXXXXbcapXXmqjTHFXX-60-60.png","link":"//www.tmall.hk/wow/import/act/jinkoubaoshui","rank":-1},{"description":"卖家为您购买的商品投保退货运费险","displayText":"赠运费险","icon":"//img.alicdn.com/tps/TB1xupxMXXXXXb3XFXXXXXXXXXX-80-80.png","link":"//service.taobao.com/support/knowledge-7602600.htm","rank":-1}],"show":true,"success":true,"titleInformation":[]},"soldAreaDataDO":{"cityData":{"allAreaSold":false,"soldAreas":[140800,230400,371200,512000,370700,460300,511500,341000,140300,430600,520200,340500,430100,110100,451100,532500,370200,131100,220700,511000,420900,510500,621100,130600,441900,220200,361000,450600,360500,620600,411700,450100,130100,330800,330300,211000,522300,441400,440900,411200,210500,321100,150600,410700,530500,620100,542300,350800,150100,440400,350300,231000,320600,610900,410200,320100,371300,533100,341600,140900,431200,230500,341100,610400,430700,520300,640100,532600,140400,370800,511600,370300,511100,340600,430200,340100,220800,451200,361100,152200,450700,130700,421000,220300,510600,330900,420500,510100,620700,442000,130200,621200,441500,360600,450200,211100,530600,360100,620200,411300,330400,522400,445100,210600,150700,350900,611000,440500,321200,410800,210100,513200,320700,150200,410300,530100,632500,231100,341700,640200,431300,222400,350400,542400,141000,230600,320200,371400,610500,370900,511700,341200,140500,430800,230100,520400,340700,430300,451300,370400,421100,510700,340200,130800,220400,450800,360700,450300,130300,331000,420600,232700,330500,420100,211200,530700,620300,441600,620800,360200,411400,210700,321300,632600,150800,410900,513300,445200,210200,150300,440600,350500,610600,440100,231200,320800,120100,640300,410400,320300,371500,542500,341800,632100,141100,230700,341300,430900,140600,230200,533300,371000,610100,622900,511800,370500,460100,511300,532300,340800,140100,152900,430400,532800,340300,451400,310100,450900,130900,421200,220500,510800,331100,420700,510300,630100,130400,441700,360800,450400,211300,360300,411500,330600,620900,420200,522600,330100,445300,210800,530300,632700,150900,441200,530800,620400,440700,411000,210300,513400,320900,542600,632200,150400,410500,500100,610700,350600,440200,533400,350100,610200,623000,230800,320400,371600,422800,371100,640400,511900,542100,140700,431000,230300,430500,520100,140200,532900,370600,460200,511400,370100,421300,510900,340400,152500,131000,220600,451000,360900,621000,450500,130500,420800,220100,510400,330700,420300,433100,211400,522700,540100,441800,441300,360400,411600,210900,411100,530900,330200,620500,522200,210400,632300,150500,440800,530400,350700,632800,440300,321000,410600,320500,542200,371700,410100,610300,230900,341500,610800,431100,350200,640500]},"currentAreaEnable":true,"regionData":{"allAreaSold":false,"soldAreas":[110113,110112,110115,110114,110117,110116,110101,110229,110228,110103,110102,110230,110105,110104,110107,110106,110109,110108,110111]},"success":true,"townData":{"allAreaSold":true,"soldAreas":[110101008,110101009,110101010,110101011,110101012,110101013,110101014,110101015,110101016,110101017,110101001,110101002,110101003,110101004,110101005,110101006,110101007]},"useNewRegionalSales":true},"tradeResult":{"cartEnable":true,"cartType":2,"miniTmallCartEnable":true,"startTime":1539584594000,"success":true,"tradeEnable":true,"tradeType":2},"userInfoDO":{"activeStatus":0,"companyPurchaseUser":false,"loginMember":false,"loginUserType":"buyer","success":true,"userId":0}},"isSuccess":true})'
    # response_json_reg = '\((.*?)\)$'
    # response_json_str = re.findall(response_json_reg, json1)[0]
    # print response_json_str
    # response_json = json.loads(response_json_str)
    # print response_json, response_json_str
