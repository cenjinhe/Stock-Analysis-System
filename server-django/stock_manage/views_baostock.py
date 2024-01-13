#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/10/29 21:51
# @File     : views_baostock.py
# @baostock : www.baostock.com
import re
import json
import time
import datetime
import pandas as pd
import baostock as bs
from django.db import connection
from django.http.response import JsonResponse
from stock_manage import models_sql
from stock_manage.utils import handler, 拟合斜率
from stock_manage.models import StockListSZ, StockListSH

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
COUNT = 3


# 更新股票历史数据(单个股票的历史数据)
def update_history_data_single(request):
    if request.method == 'PUT':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market', '1')
        stock_code = json_param.get('code')
        release_date = json_param.get('release_date')
        str_code = f'SZ.{stock_code}' if str(market) == '1' else f'SH.{stock_code}'
        table = TABLE_MAP.get(str(market))

        _update_stock(market, stock_code, release_date, str_code, table)
    return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})


# 更新股票历史数据(所有股票的历史数据)
def update_history_data_all(request):
    if request.method == 'PUT':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')
        for market in [1, 0]:
            table = TABLE_MAP.get(str(market))
            records = table.objects.all()
            for record in records:
                if record.status:
                    continue
                str_code = f'SZ.{record.code}' if str(market) == '1' else f'SH.{record.code}'
                _update_stock(market, record.code, record.date, str_code, table)
    return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})


# 更新个股
def _update_stock(market, stock_code, release_date, code, table):
    # 更新股票列表的状态（status: true更新中）
    record = table.objects.filter(code=stock_code).first()
    if record.status:
        return JsonResponse({'data': {}, 'code': '201', 'message': f'该股票code={code}正在更新中...'})
    table.objects.filter(code=stock_code).update(status=True,
                                                 update_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()))

    try:
        # 如果数据库表不存在，则创建
        sql = f'{models_sql.CREATE_TABLE_HISTORY_DATA}'.format(TABLE_NAME=f'tb_{stock_code}')
        with connection.cursor() as cursor:
            cursor.execute(sql)
        # 获取数据入库的开始日期(数据库中最近的1条记录时间)
        sql = f'{models_sql.SELECT_MAX_DATE}'.format(TABLE_NAME=f'tb_{stock_code}')
        with connection.cursor() as cursor:
            cursor.execute(sql)
            last_date = cursor.fetchall()
        condition = last_date is not None and last_date[0][0] is not None
        start_date = last_date[0][0].strftime('%Y-%m-%d') if condition else release_date
        start_date = str(start_date)
        # 获取数据入库的结束日期(当天)
        end_date = datetime.datetime.now().date()
        end_date = end_date.strftime("%Y-%m-%d")

        # 登陆证券宝系统,获取历史数据
        bs.login()
        fields = "date, code, open, high, low, close, preclose, volume, amount, adjustflag, turn, tradestatus, " \
                 "pctChg, peTTM, pbMRQ, psTTM, pcfNcfTTM, isST"
        print('获取历史数据参数：', f'market={market}', f'code={code}', f'start_date={start_date}', f'end_date={end_date}')
        respond = bs.query_history_k_data(code=code, fields=fields, start_date=start_date, end_date=end_date)
        data_list = []
        while (respond.error_code == '0') & respond.next():  # 获取一条记录，将记录合并在一起
            data_list.append(respond.get_row_data())
        result = pd.DataFrame(data_list, columns=respond.fields)

        # 将历史数据更新到数据库
        for index, row in result.iterrows():
            # 判断row['date']日期的数据是否已存在（存在：更新/不存在：添加）
            sql = f'{models_sql.SELECT_DATA_WHERE_DATE}'.format(TABLE_NAME=f'tb_{stock_code}', date=row['date'])
            with connection.cursor() as cursor:
                cursor.execute(sql)
                data = cursor.fetchall()
            # 增加历史数据 or 更新历史数据
            sql = models_sql.INSERT_INTO_HISTORY_DATA if data[0][0] == 0 else models_sql.UPDATE_HISTORY_DATA
            sql = sql.format(
                TABLE_NAME=f'tb_{stock_code}',
                date=row['date'],                                                       # 行情日期
                code=re.findall(r'\d+\.?\d*', row['code'])[0],                          # 股票代码
                open=row['open'] if row['open'] != '' else 0,
                high=row['high'] if row['high'] != '' else 0,
                low=row['low'] if row['low'] != '' else 0,
                close=row['close'] if row['close'] != '' else 0,
                pre_close=row['preclose'] if row['preclose'] != '' else 0,
                volume=row['volume'] if row['volume'] != '' else 0,
                amount=row['amount'] if row['amount'] != '' else 0,
                adjust_flag=row['adjustflag'] if row['adjustflag'] != '' else 0,
                turn=row['turn'] if row['turn'] != '' else 0,
                trade_status=row['tradestatus'] if row['tradestatus'] != '' else 0,
                pctChg=row['pctChg'] if row['pctChg'] != '' else 0,
                peTTM=row['peTTM'] if row['peTTM'] != '' else 0,
                pbMRQ=row['pbMRQ'] if row['pbMRQ'] != '' else 0,
                psTTM=row['psTTM'] if row['psTTM'] != '' else 0,
                pcfNcfTTM=row['pcfNcfTTM'] if row['pcfNcfTTM'] != '' else 0,
                isST=row['isST'] if row['isST'] != '' else 0)
            with connection.cursor() as cursor:
                print(f'sql={sql}')
                cursor.execute(sql)

            # try:
            #     # ######### 添加字段pre_trend_status ########
            #     sql = f"ALTER TABLE tb_{stock_code} ADD COLUMN pre_trend_status char(50) DEFAULT NULL COMMENT '前回斜率状态' AFTER trend_status"
            #     with connection.cursor() as cursor:
            #         cursor.execute(sql)
            # except:
            #     pass

            # 获取原始数据COUNT件，计算趋势and斜率，并更新到数据库
            pre_result = 拟合斜率.getPreSlopeAndTrend(stock_code, row['date'], COUNT)
            result = 拟合斜率.getSlopeAndTrend(stock_code, row['date'], COUNT)
            sql = models_sql.UPDATE_TREND_PRE_AND_CUR.format(
                TABLE_NAME=f'tb_{stock_code}',
                slope=result['slope'],                        # 斜率
                intercept=result['intercept'],                # 截距
                pre_trend_status=pre_result['trend_status'],  # 前回斜率状态["上升", "下降", "波动", "平稳"]
                trend_status=result['trend_status'],          # 当前斜率状态["上升", "下降", "波动", "平稳"]
                date=row['date'])
            with connection.cursor() as cursor:
                cursor.execute(sql)
    finally:
        _update_stock_list(table, stock_code)


# 更新股票列表(个股更新后，将最近一条数据如，最高价，现价等等更新到股票列表中)
def _update_stock_list(table, stock_code):
    # 查询这个表的最后一条数据
    lastData = handler.getRawDataDict(stock_code, 1)
    today_date = lastData[0]['date'] if lastData else None
    open = lastData[0]['open'] if lastData else None
    high = lastData[0]['high'] if lastData else None
    low = lastData[0]['low'] if lastData else None
    close = lastData[0]['close'] if lastData else None
    pre_close = lastData[0]['pre_close'] if lastData else None
    volume = lastData[0]['volume'] if lastData else None
    amount = lastData[0]['amount'] if lastData else None
    adjust_flag = lastData[0]['adjust_flag'] if lastData else None
    turn = lastData[0]['turn'] if lastData else None
    trade_status = lastData[0]['trade_status'] if lastData else None
    pctChg = lastData[0]['pctChg'] if lastData else None
    slope = lastData[0]['slope'] if lastData else None
    intercept = lastData[0]['intercept'] if lastData else None
    trend_status = lastData[0]['trend_status'] if lastData else None
    pre_trend_status = lastData[0]['pre_trend_status'] if lastData else None
    # 更新股票列表的状态（status: False） and 更新股票列表的更新时间（update_time）,及股票信息
    record = table.objects.filter(code=stock_code).first()
    table.objects.filter(code=stock_code).update(
        update_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        today_date=today_date,  # 当前行情日期
        open=open,              # 开盘价
        high=high,              # 最高价
        low=low,                # 最低价
        close=close,            # 收盘价
        pre_close=pre_close,    # 前一天收盘价
        ratio='{:.2f}'.format(pctChg) if pctChg else 0,  # 涨跌幅
        trade_status=trade_status if record.trade_status != 2 else record.trade_status,  # 退市交易状态不变
        status=False,                        # 更新状态
        slope=slope,                         # 斜率
        intercept=intercept,                 # 截距
        trend_status=trend_status,           # 当前斜率状态
        pre_trend_status=pre_trend_status    # 前回斜率状态
    )

