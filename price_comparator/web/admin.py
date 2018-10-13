# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Goods


def disable_needs_update(modeladmin, request, queryset):
    queryset.update(needs_update=False)


def enable_needs_update(modeladmin, request, queryset):
    queryset.update(needs_update=True)


class GoodsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'g_name', 'needs_update', 'g_url', 'g_from', 'price_lasted', 'price_moniter', 'stock', 'status',
        'date_created', 'date_updated', 'category')
    list_display_links = ('id', 'g_name')
    list_filter = ('g_from', 'needs_update', 'status')
    search_fields = ['g_name', 'g_url']
    actions = [disable_needs_update, enable_needs_update]


# Register your models here.
admin.site.register(Goods, GoodsAdmin)
