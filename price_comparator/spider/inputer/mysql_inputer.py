# -*- coding=utf-8 -*-
from web.models import Goods


class Mysql_inputer:
    @staticmethod
    def get_input():
        goods = Goods.objects.filter(status=1)
        return goods