# -*- coding: utf-8 -*-
from price_comparator.spider.inputer.mysql_inputer import Mysql_inputer
import logging

def run_program():
    # 拉取全部商品 TODO 分页
    print(1111111111111111111111111111111111111111111)
    logging.info("spider_starting ====")
    goods_list = Mysql_inputer.get_input()
    # 调用processer进行处理
    logging.info("spider_doing ====")
    print(goods_list[1].id)

    # 打印需变更结果

