#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2022/12/10 22:34
# @File     : script_trendline.py

"""
1.做最小二乘拟合，把序列拟合成一条直线;
2.根据直线的斜率k可以得知序列的主要走势：
例如：(1)k > 0.1763 上升  (2) k < -0.1763 下降 (3)其他
3.然后计算序列各点到直线的距离（和方差一样）
设定一个阈值L，统计超过L的点数目，点数目越多说明序列震荡越厉害
"""
import numpy as np
import math


def trendline(data):
    """
    拟合曲线
    """
    order = 2
    index = [i for i in range(1, len(data) + 1)]   # x轴坐标
    coeffs = np.polyfit(index, list(data), order)  # 曲线拟合
    # k = coeffs[0] # 斜率
    print('斜率:', coeffs)
    return coeffs


def judge_slope(coeffs, data, degree, shake=1):
    tan_k = math.tan(degree * math.pi / 180)  # 注意弧度转化
    # print(coeffs[0])
    print('tan_k=', tan_k)
    if coeffs[0] >= tan_k:
        return "上升"
    elif coeffs[0] <= -tan_k:
        return "下降"
    else:
        return get_shake(coeffs, data, shake)


def get_shake(coeffs, data, shake):
    count = 0
    for i, d in enumerate(data):  # i+1相当于横坐标，从1开始
        y = np.polyval(coeffs, i + 1)
        count += (y - d) ** 2
    print("count: ", count)
    if count > shake:
        return "波动"
    else:
        return "平稳"


def get_data(code, num):
    # stock_code = '002688'
    # data_num = 22
    # connect_history = MSSQL(host=HOST, user=USER, pwd=PWD, db=DB_HISTORY)
    # sql = f'{sql_context.SELECT_CLOSE_PRICE_WHERE_CODE}'.format(data_num=data_num, stock_code=stock_code)
    # result = connect_history.ExecQuery_2(sql)
    data = []
    # for i in range(len(result)):
    #     data.append(float(result[i]['CLOSE_PRICE']))

    return data


if __name__ == '__main__':
    data = get_data()
    coeffs = trendline(data)

    res = judge_slope(coeffs, data, degree=1, shake=1)
    print(res)
