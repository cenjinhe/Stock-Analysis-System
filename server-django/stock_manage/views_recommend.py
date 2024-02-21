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
from stock_manage.utils import handler, 拟合斜率, macd
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
COUNT = 200


# 更新股票推荐分析结果
def postUpdateStockRecommend(request):
    if request.method == 'POST':
        # 遍历[深市, 沪市]
        for market in [1]:
            # 分别获取[深市, 沪市]的股票列表
            queryset = TABLE_MAP.get(str(market)).objects.all().values()
            data = list(queryset)
            # 遍历股票列表
            # for row in data:
            for row in data[0:1]:
                code = row['code']
                rawData = handler.getRawDataList(code, COUNT)
                if len(rawData) > 0:
                    # 获取data，如:[[日期(date), 开盘(open)，收盘(close)，最低(low)，最高(high)]]，并倒序(日期从小到大)
                    data = [[element[0], element[1], element[2], element[3], element[4]] for element in rawData][::-1]
                    # print('data=', data)
                    # 计算MACD指标
                    macd_data, dif_data, dea_data = macd.calculateMACD(10, 21, 9, data, 2)
                    print('macd_data=', macd_data)
                    print('dif_data=', dif_data)
                    print('dea_data=', dea_data)


        # 3根据code，计算x-1日上次的斜率状态
        # 4根据code，更新或插入数据
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")

