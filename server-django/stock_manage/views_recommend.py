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
                    closeData = [element[2] for element in rawData][::-1]
                    print('closeData=', closeData)
                    # 计算MACD

        # 3根据code，计算x-1日上次的斜率状态
        # 4根据code，更新或插入数据
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")

