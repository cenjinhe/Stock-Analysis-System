import os
import json
import pandas as pd
from datetime import datetime
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from stock_manage.models import StockListSZ, StockListSH


# 获取股票列表
def getStockList(request):
    TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
    if request.method == 'GET':
        size = request.GET.get('size', default=10)
        current = request.GET.get('current', default=1)
        code = request.GET.get('code', default='')
        name = request.GET.get('name', default='')
        stockExchange = request.GET.get('stockExchange', default='1')

        listData = []
        records = TABLE_MAP.get(stockExchange).objects.filter(code__contains=code, name__contains=name)
        page_info = Paginator(records, size).page(number=current)
        for record in page_info:
            listData.append({"id": record.id,
                             "code": record.code,
                             "name": record.name,
                             "date": record.date,
                             "update_time": record.update_time.strftime("%Y-%m-%d %H:%M:%S")})
        json_data = {'list': listData, 'total': len(records)}
        return JsonResponse({'data': json_data, 'code': '200', 'message': '获取成功!'})


# 更新股票列表toDB
def updateStockList(request):
    TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
    FILE_MAP = {'0': 'shA股列表.csv', '1': 'szA股列表.csv'}
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        stockExchange = json_param.get('stockExchange', 1) if json_param else 1
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scv_file = os.path.join(BASE_DIR, 'stock_manage', 'data', FILE_MAP.get(str(stockExchange)))
        df = pd.read_csv(scv_file, dtype={"A股代码": "object"})
        for i in range(len(df)):
            code = df['A股代码'][i]
            name = df['A股简称'][i] if stockExchange == 1 else df['证券简称'][i]
            date = df['上市日期'][i] if stockExchange == 1 else datetime.strptime(str(df['上市日期'][i]), "%Y%m%d").strftime('%Y-%m-%d')
            date = datetime.strptime(date, "%Y-%m-%d").date()
            # 如果数据库中没有这条A股代码，就添加
            record = TABLE_MAP.get(str(stockExchange)).objects.filter(code__exact=code)
            if len(record) == 0:
                TABLE_MAP.get(str(stockExchange)).objects.create(code=code, name=name, date=date)

        return JsonResponse({'data': {}, 'code': '200', 'message': '获取成功!'})

