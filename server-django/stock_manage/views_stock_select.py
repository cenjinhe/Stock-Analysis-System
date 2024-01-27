import os
import json
import pandas as pd
from datetime import datetime
from django.db import connection
from django.http import HttpResponse
from django.forms import model_to_dict
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from stock_manage import models_sql
from stock_manage.utils import handler, 拟合斜率
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}


# 更新股票分析结果-斜率状态
def postUpdateStockSelect(request):
    if request.method == 'POST':
        for market in [1, 0]:
            # 分别获取[深市, 沪市]的股票列表
            queryset = TABLE_MAP.get(str(market)).objects.all().values()
            data = list(queryset)
            # 遍历股票列表
            for row in data:
                code = row['code']
                print('market=', market, 'code=', code)
                # rawData = handler.getRawDataList(code, 7)
                # if len(rawData) > 0:
                #     closeData = [element[2] for element in rawData][::-1]
                #     slope, intercept = 拟合斜率.trend_line(closeData)
                #     trend_status = 拟合斜率.judge_trend((slope, intercept), closeData)
                #     print(f'trend_status={trend_status}')
                #     sql = models_sql.UPDATE_TREND.format(
                #         TABLE_NAME=f'tb_{stock_code}',
                #         slope='{:.6f}'.format(slope),                # 斜率
                #         intercept='{:.6f}'.format(intercept),        # 截距
                #         trend_status=trend_status,                   # 斜率状态["上升", "下降", "波动", "平稳"]
                #         date=row['date'])
                #     with connection.cursor() as cursor:
                #         cursor.execute(sql)
        # 3根据code，计算x-1日上次的斜率状态
        # 4根据code，更新或插入数据
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")
