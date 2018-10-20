# -*- coding=utf-8 -*-
from django.db.models import Q
from web.models import Goods


class Mysql_inputer:
    @staticmethod
    def get_input(status_min, status_max):
        goods = Goods.objects.filter(Q(status__gte=status_min) & Q(status__lte=status_max))
        return goods