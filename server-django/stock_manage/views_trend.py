import os
import json
import pandas as pd
from datetime import datetime
from django.db import connection
from django.http import HttpResponse
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from config import models_sql
from stock_manage.utils import handler, 拟合斜率
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}


# 获取最近上升趋势变化的数据列表
def getUpTrendDataList(request):
    if request.method == 'GET':
        count = request.GET.get('count', default=7)
        code = request.GET.get('code', default='')
        market = request.GET.get('market', default='1')
        retData = []

        # 获取A股简称
        table = TABLE_MAP.get(str(market))
        record = table.objects.filter(code=code).first()
        name = record.name if record else ''
        if str(market) == '1' and name == '':
            # 如果在深市列表中没有获取到简称，将尝试在沪市列表中获取
            table = TABLE_MAP.get('0')
            record = table.objects.filter(code=code).first()
            name = record.name if record else ''

        flg = True
        upFirst = False
        index = 1
        while flg:
            # 获取当前行的数据
            data = handler.getRawDataDict(code, index)
            if len(data) != index:
                flg = False  # 跳出while循环
                continue
            data = data[index - 1:index]
            date = data[0]['date']
            close = data[0]['close']

            # 获取原始数据count件，计算趋势and斜率
            result = 拟合斜率.getSlopeAndTrend(code, date, count)
            slope = result['slope']
            trend_status = result['trend_status']

            # 保存到retData中
            retData.append({
                'date': date,
                'code': code,
                'name': name,
                'close': close,
                'slope': slope,
                'trend_status': trend_status,
            })

            # 判读是否跳出while循环
            if trend_status != '上升' and upFirst:
                flg = False  # 跳出while循环
                continue
            if trend_status == '上升' and not upFirst:
                upFirst = True
            index += 1

        return JsonResponse({'rawData': retData, 'code': '200', 'message': '获取成功!'})


# 更新股票分析结果-斜率状态
def postUpdateTrendStatus(request):
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')

        # 通过调用values()方法将Model的所有对象转换为字典，并将这些字典存储在名为data的列表中
        queryset = TABLE_MAP.get(str(market)).objects.all().values()
        data = list(queryset)

        # 遍历股票列表
        for row in data:
            # 根据code，获取原始数据7件，计算趋势and斜率，并更新到数据库
            code = row['code']
            rawData = handler.getRawDataList(code, 7)
            if len(rawData) > 0:
                closeData = [element[2] for element in rawData][::-1]
                slope, intercept = 拟合斜率.trend_line(closeData)
                trend_status = 拟合斜率.judge_trend((slope, intercept), closeData)
                print(f'trend_status={trend_status}')
                # sql = models_sql.UPDATE_TREND.format(
                #     TABLE_NAME=f'tb_{stock_code}',
                #     slope='{:.6f}'.format(slope),                # 斜率
                #     intercept='{:.6f}'.format(intercept),        # 截距
                #     trend_status=trend_status,                   # 斜率状态["上升", "下降", "波动", "平稳"]
                #     date=row['date'])
                # with connection.cursor() as cursor:
                #     cursor.execute(sql)
        # 3根据code，计算x-1日上次的斜率状态
        # 4根据code，更新或插入数据
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")
