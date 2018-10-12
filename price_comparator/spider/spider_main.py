# -*- coding: utf-8 -*-
from price_comparator.spider.inputer.mysql_inputer import Mysql_inputer


def run_program():
    # 拉取全部商品 TODO 分页
    goods_list = Mysql_inputer.get_input()
    # 调用processer进行处理
    print goods_list[1].id
    # 打印需变更结果

