#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Description: 计算 MACD 指标
# @Author   : jinhe Cen
# @Time     : 2024/2/20 23:09
# @File     : macd.py


# EMA指数平滑移动平均线(= DEA)
def calculateEMA(n, data, field=1):
    """
    :param n: short 快速EMA or long 慢速EMA
    :param data: 数据
    :param field: 计算字段配置
    :return: EMA
    """
    a = 2 / (n + 1)
    if field:
        # 二维数组
        ema = [data[0][field]]
        length = len(data)
        i = 1
        while i < length:
            ema.push((a * data[i][field] + (1 - a) * ema[i - 1]).toFixed(3))
            i += 1
    else:
        # 普通一维数组
        ema = [data[0]]
        length = len(data)
        i = 1
        while i < length:
            ema.push((a * data[i] + (1 - a) * ema[i - 1]).toFixed(3))
            i += 1
    return ema


# DIF快线
def calculateDIF(short, long, data, field=1):
    """
    :param short: 快速EMA
    :param long: 慢速EMA
    :param data: 数据
    :param field: 计算字段配置
    :return: DIF
    """
    dif = []
    emaShort = calculateEMA(short, data, field)
    emaLong = calculateEMA(long, data, field)
    length = len(data)
    i = 0
    while i < length:
        dif.push((emaShort[i] - emaLong[i]).toFixed(3))
        i += 1
    return dif


# MACD指标
def calculateMACD(short=12, long=26, mid=9, data=None, field=1):
    """
    :param short: 快速EMA
    :param long: 慢速EMA
    :param mid: dea时间窗口
    :param data: 数据
    :param field: 计算字段配置
    :return: {macdData, diffData, deaData}
    """
    if data is None:
        data = []

    macdData = []
    diffData = calculateDIF(short, long, data, field)
    deaData = calculateEMA(mid, diffData)
    length = len(data)
    i = 0
    while i < length:
        macdData.push(((diffData[i] - deaData[i]) * 2).toFixed(3))
        i += 1
    return {macdData, diffData, deaData}
