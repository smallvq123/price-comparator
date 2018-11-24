# -*- coding=utf-8 -*-
import random

header_taobao = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.3',
    'Referer': 'https://item.taobao.com/item.htm',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Connection': 'keep-alive',
}

header_tmall_detail = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.3',
    'Referer': 'https://list.tmall.com/search_product.htm?q=',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Connection': 'keep-alive',
}

headers_price_tmall = {
    'Host': "mdskip.taobao.com",
    'cookie': 'miid=885221573714943798; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=smallvq; _cc_=WqG3DMC9EA%3D%3D; tg=0; l=ArS04f0dgYQRMtMqetwpb6bSBHkmodh3; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; cna=SxxBE1l5qUoCAXx+Ctpm91B2; t=1cfd8b51a76498782dd5e6ec4d3497c4; _m_h5_tk=399d5715e5cf175478fde01e94b0be21_1539452633139; _m_h5_tk_enc=86aa3f2242fd574041c9c084a2751f8f; enc=7NWQLSMAccpJZGROiBoxd1CpIV9Ky23cSV7KnHMuJSmelEF%2BJVlLLF%2BZhilwY7usDC5o0uNY9BZw2BPfqWKGyQ%3D%3D; cookie2=13dc7987eb19c597e0db9d2b1ad3d77d; v=0; _tb_token_=e4e56e58d65ee; mt=ci=22_1&np=; isg=BOXl3N950iAlrTfpgNYqfHr59KEVzKZkDfzS0ufKIpwr_gVwr3KphHOUjGKIfrFs',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Referer': 'http://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.12.UpuePQ&is_b=1&id=' + str(
        random.randint(15486609514, 15486629514))
}

headers_innisfree = {
    'Host': "www.innisfree.cn",
    'Cookie': '',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Referer': 'https://www.innisfree.cn/Product.do?method=productView&seq=' + str(
        random.randint(1000001222, 1000007222))
}

headers_etude = {
    'Host': "www.etude.cn",
    'Accept': '*/*',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'x-et-token': '1f0eb65a747016868c11018a69d174b2',
    'Origin': 'http://www.etude.cn',
    'Cookie': 'WHATAP=x44ikil2ne0cgc; gr_user_id=2863dc9a-aee1-43ad-8509-4d3039fca7ab; grwng_uid=b16ce84c-3020-45bf-a0e6-65f49515bf83; 9a295692db079be1_gr_session_id=ec29703f-f938-48b2-8c8c-7be5dde46968; JSESSIONID=1FBEB6C56886DB3005C8726E8939CD17; 9a295692db079be1_gr_session_id_ec29703f-f938-48b2-8c8c-7be5dde46968=true',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'Referer': 'http://www.etude.cn/product.html?prdCode=' + str(
        random.randint(100018520, 100019520))
}
