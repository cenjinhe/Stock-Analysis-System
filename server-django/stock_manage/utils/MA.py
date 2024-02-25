#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: 计算 MA 均线数据
# @Author   : jinhe Cen
# @Time     : 2024/2/25 12:17
# @File     : MA.py


# 计算 MA 均线数据
def calculateMA(dayCount, data, field=1):
    """
    :param dayCount: 几日均线
    :param data: 数据
    :param field: 计算数据的哪个字段,如: 收盘(close)
    :return: 均线数据
    """
    result = []
    length = len(data)
    for i in range(length):
        if i < dayCount:
            result.append('-')
            continue
        total = 0
        # 取dayCount的合计
        for j in range(dayCount):
            total += float(data[i - j][field])
        # 取dayCount的平均值,保留2位小数
        element = total / dayCount
        result.append('{:.2f}'.format(element))
    return result
