#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/11/19 16:41
# @File     : 拟合斜率.py
"""
功能
1.通过斜率法计算，选出所有股票：前一天斜率 及当前斜率
2.将计算出来的斜率更新到stock_list_sz数据库表，关联字段(pre_trend,trend)
说明
方法一 斜率法
    原理
    斜率法的原理就是使用最小二乘等方法对时序数据进行拟合，
    然后根据拟合成的直线的斜率k判断序列的数据走势，
    当k>0时，则代表趋势上升；当k<0时，则代表趋势下降。
    优缺点
    优点是方法简单；缺点是要求趋势是线性的，当数去波动较大时无法准确拟合。

    https://www.cnblogs.com/yibeimingyue/p/11185535.html
"""
import math
import numpy as np
from stock_manage.utils import handler


def _trend_line(data):
    """做最⼩⼆乘拟合，把数据拟合成⼀条直线"""
    x = [i for i in range(1, len(data) + 1)]  # x 坐标
    y = list(data)  # y 坐标
    slope, intercept = np.polyfit(x, y, deg=1)  # 拟合曲线
    return slope, intercept  # slope：斜率 intercept：截距


def _judge_trend(coeffs, data, degree=1, shake=1):
    """根据直线的斜率k，判断数据的主要⾛势"""
    tan_k = math.tan(degree * math.pi / 180)  # tan()返回x弧度的正切值，数值在 -1 到 1 之间
    # print('tan_k=', tan_k)  # tan_k= 0.017455064928217585
    if coeffs[0] >= tan_k:
        return "上升"
    elif coeffs[0] <= -tan_k:
        return "下降"
    else:
        return _get_shake(coeffs, data, shake)


def _get_shake(coeffs, data, shake):
    count = 0
    for i, d in enumerate(data):  # i+1相当于横坐标，从1开始
        y = np.polyval(coeffs, i + 1)
        count += (y - d) ** 2
    # print("count: ", count)
    if count > shake:
        return "波动"
    else:
        return "平稳"


# 计算(现在的)趋势and斜率
def getSlopeAndTrend(code, date, count):
    """
    获取原始数据count件，计算趋势and斜率
    slope: 斜率
    intercept: 截距
    trend_status: 斜率状态["上升", "下降", "波动", "平稳"]
    """
    retData = {'slope': 0, 'intercept': 0, 'trend_status': ''}
    rawData = handler.getRawDataListFromEndDate(code, date, count)
    if len(rawData) > 0:
        closeData = [element[2] for element in rawData][::-1]
        slope, intercept = _trend_line(closeData)
        trend_status = _judge_trend((slope, intercept), closeData)
        retData = {'slope': '{:.6f}'.format(slope),
                   'intercept': '{:.6f}'.format(intercept),
                   'trend_status': trend_status}
    return retData


# 计算(前一天的)趋势and斜率
def getPreSlopeAndTrend(code, date, count):
    """
    获取原始数据count件，计算(前回的)趋势and斜率
    slope: 斜率
    intercept: 截距
    trend_status: 斜率状态["上升", "下降", "波动", "平稳"]
    """
    retData = {'slope': 0, 'intercept': 0, 'trend_status': ''}
    rawData = handler.getRawDataListFromDate(code, date, count + 1)
    if len(rawData) > 1:
        rawData = rawData[1:]
        closeData = [element[2] for element in rawData][::-1]
        slope, intercept = _trend_line(closeData)
        trend_status = _judge_trend((slope, intercept), closeData)
        retData = {'slope': '{:.6f}'.format(slope),
                   'intercept': '{:.6f}'.format(intercept),
                   'trend_status': trend_status}
    return retData


# 根据数据,直接计算趋势and斜率
def getSlopeAndTrendByData(data, field=0):
    """
    :param data: 数据
    :param field: 计算数据的哪个字段,如: 收盘(close)
    :return: 斜率,截距,斜率状态
    """
    retData = {'slope': 0, 'intercept': 0, 'trend_status': ''}
    rawData = data
    if field:
        # 二维数组
        if len(rawData) > 0:
            closeData = [element[field] for element in rawData]
            slope, intercept = _trend_line(closeData)
            trend_status = _judge_trend((slope, intercept), closeData)
            retData = {'slope': '{:.6f}'.format(slope),
                       'intercept': '{:.6f}'.format(intercept),
                       'trend_status': trend_status}
    else:
        # 普通一维数组
        if len(rawData) > 0:
            closeData = [float(element) for element in rawData]
            slope, intercept = _trend_line(closeData)
            trend_status = _judge_trend((slope, intercept), closeData)
            retData = {'slope': '{:.6f}'.format(slope),
                       'intercept': '{:.6f}'.format(intercept),
                       'trend_status': trend_status}
    return retData
