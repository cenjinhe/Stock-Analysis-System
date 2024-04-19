#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/11/22 21:38
# @File     : handler.py
from django.db import connection
from config import models_sql


def getRawDataListFromStartDate(code, endDate, count):
    """
    根据开始日期,获取原始数据列表([字典])
    """
    newData = []
    try:
        if str(count) == '0':
            sql = f'{models_sql.SELECT_RAW_DATA_ALL_FROM_START_DATE}'.format(TABLE_NAME=f'tb_{code}', DATE=endDate)
        else:
            sql = f'{models_sql.SELECT_RAW_DATA_FROM_START_DATE}'.format(TABLE_NAME=f'tb_{code}',
                                                                         DATE=endDate, COUNT=count)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            # 获取结果
            rawData = cursor.fetchall()
            # 获取字段名
            fieldDict = _get_field_dict(cursor)
            # 转化成dict格式（默认是tuple格式）
            for data in rawData:
                temp = dict()
                for field in fieldDict:
                    temp[field] = data[fieldDict[field]]
                newData.append(temp)
    except Exception as ex:
        pass
    # 倒序, 行情日期从小到大排序
    newData = newData[::-1] if newData else []
    return newData


def getRawDataListFromEndDate(code, endDate, count):
    """
    根据终了日期,获取原始数据列表(元组)
    """
    rawData = ()
    try:
        if str(count) == '0':
            sql = f'{models_sql.SELECT_RAW_DATA_ALL_FROM_END_DATE}'.format(TABLE_NAME=f'tb_{code}', DATE=endDate)
        else:
            sql = f'{models_sql.SELECT_RAW_DATA_FROM_END_DATE}'.format(TABLE_NAME=f'tb_{code}',
                                                                       DATE=endDate, COUNT=count)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rawData = cursor.fetchall()
    except Exception as ex:
        pass
    return rawData


def getRawDataList(code, count):
    """
    获取原始数据列表(元组)
    """
    rawData = ()
    try:
        if str(count) == '0':
            sql = f'{models_sql.SELECT_RAW_DATA_ALL}'.format(TABLE_NAME=f'tb_{code}')
        else:
            sql = f'{models_sql.SELECT_RAW_DATA}'.format(TABLE_NAME=f'tb_{code}', COUNT=count)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rawData = cursor.fetchall()
    except Exception as ex:
        pass
    return rawData


def getRawDataDict(code, count):
    """
    获取原始数据列表([字典])
    """
    newData = []
    try:
        if str(count) == '0':
            sql = f'{models_sql.SELECT_RAW_DATA_ALL_MORE}'.format(TABLE_NAME=f'tb_{code}')
        else:
            sql = f'{models_sql.SELECT_RAW_DATA_MORE}'.format(TABLE_NAME=f'tb_{code}', COUNT=count)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            # 获取结果
            rawData = cursor.fetchall()
            # 获取字段名
            fieldDict = _get_field_dict(cursor)
            # 转化成dict格式（默认是tuple格式）
            for data in rawData:
                temp = dict()
                for field in fieldDict:
                    temp[field] = data[fieldDict[field]]
                newData.append(temp)
    except Exception as ex:
        pass
    return newData


def _get_field_dict(cursor):
    """
    获取数据库对应表中的字段名
    """
    index_dict = dict()
    index = 0
    for desc in cursor.description:
        index_dict[desc[0]] = index
        index = index + 1
    return index_dict
