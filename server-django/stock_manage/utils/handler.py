#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/11/22 21:38
# @File     : handler.py
from django.db import connection
from stock_manage import models_sql


# 获取原始数据列表
def getRawDataList(code, count):
    if str(count) == '0':
        sql = f'{models_sql.SELECT_RAW_DATA_ALL}'.format(TABLE_NAME=f'tb_{code}')
    else:
        sql = f'{models_sql.SELECT_RAW_DATA}'.format(TABLE_NAME=f'tb_{code}', COUNT=count)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rawData = cursor.fetchall()
    return rawData
