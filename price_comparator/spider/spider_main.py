# -*- coding: utf-8 -*-
from inputer.mysql_inputer import Mysql_inputer
import logging

from processer import spider_processer


# status_min最小status范围 >= status_min
# status_max 最大status <=status_max
def run_program(status_min, status_max):
    if status_min == None:
        status_min = 1
        status_max = 1
    # 拉取全部商品 TODO 分页
    logging.info("spider_starting ====")
    goods_list = Mysql_inputer.get_input(status_min, status_max)
    # 调用processer进行处理
    logging.info("spider_doing ====")
    spider_processer.Processer().process(goods_list)
    logging.info("spider_ending ====")
    # 打印需变更结果
    return True

def cron_program():
    logging.info("crontab starting =========")
    run_program(1, 2)
    logging.info("crontab end =========")
