# -*- coding: utf-8 -*-
from inputer.mysql_inputer import Mysql_inputer
import logging

from processer import spider_processer


def run_program():
    # 拉取全部商品 TODO 分页
    print("spider_starting ====")
    logging.info("spider_starting ====")
    goods_list = Mysql_inputer.get_input()
    # 调用processer进行处理
    logging.info("spider_doing ====")
    spider_processer.Processer().process(goods_list)
    logging.info("spider_ending ====")
    # 打印需变更结果
    return True
