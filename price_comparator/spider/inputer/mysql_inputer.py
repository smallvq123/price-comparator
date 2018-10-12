# -*- coding=utf-8 -*-
from price_comparator.web.models import Goods


class Mysql_inputer:
    @staticmethod
    def get_input():
        goods = Goods.objects.filter(status_choices=1).values_list()
        return goods