# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Goods

def disable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=False)

def enable_commentstatus(modeladmin, request, queryset):
    queryset.update(is_enable=True)

class GoodsAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'g_url', 'g_from', 'g_name', 'price_lasted', 'price_moniter', 'needs_update', 'stock', 'status',
    'date_created', 'date_updated', 'category')
    list_display_links = ('id', 'commentator')
    list_filter = ('commentator', 'article', 'is_enable')
    actions = [disable_commentstatus, enable_commentstatus]


# Register your models here.
admin.site.register(Goods, GoodsAdmin)
