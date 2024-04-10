#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2024/4/10 22:41
# @File     : StockConfig.py
from stock_manage.models import StockConfig


def getConfigValue(name):
    """ 获取config """
    record = StockConfig.objects.filter(name=name).first()
    retValue = record.value if record else ''
    return retValue


def setConfigValue(name, value):
    """ 更新config """
    record = StockConfig.objects.filter(name=name).first()
    if record:
        # 更新
        StockConfig.objects.filter(name=name).update(value=value)
    else:
        # 增加
        StockConfig.objects.create(name=name, value=value)
