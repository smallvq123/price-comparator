# -*- coding: utf-8 -*-
import logging

from django.core import serializers
from django.http import JsonResponse



from models import Goods
from spider import spider_main



def test(request):
    logging.info(1111)
    spider_main.run_program()
    return JsonResponse('success', safe=False)
