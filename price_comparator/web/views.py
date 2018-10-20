# -*- coding: utf-8 -*-
import logging

from django.http import JsonResponse

from spider import spider_main


def test(request):
    status_min = request.GET.get('status_min')
    status_max = request.GET.get('status_max')
    spider_main.run_program(status_min, status_max)
    return JsonResponse('success', safe=False)
