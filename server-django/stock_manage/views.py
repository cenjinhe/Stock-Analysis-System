import os
import json
import pandas as pd
from datetime import datetime
from django.db import connection
from stock_manage import models_sql
from django.http import HttpResponse
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
        market = request.GET.get('market', default='1')

        listData = []
        records = TABLE_MAP.get(market).objects.filter(code__contains=code, name__contains=name).order_by('code')
        page_info = Paginator(records, size).page(number=current)
        for record in page_info:
            # 如果表不存在就建立这个表
            sql = f'{models_sql.CREATE_TABLE_HISTORY_DATA}'.format(TABLE_NAME=f'tb_{record.code}')
            with connection.cursor() as cursor:
                cursor.execute(sql)
            # 查询这个表的最后一条数据，获取日期
            sql = f'{models_sql.SELECT_LAST_DATA}'.format(TABLE_NAME=f'tb_{record.code}')
            with connection.cursor() as cursor:
                cursor.execute(sql)
                last_data = cursor.fetchall()
            # 加入到数据列表中
            listData.append({"id": record.id,
                             "code": record.code,
                             "name": record.name,
                             "date": record.date,
                             "close": last_data[0][6] if last_data else None,
                             "status": record.status,
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
        market = json_param.get('market')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        scv_file = os.path.join(BASE_DIR, 'stock_manage', 'data', FILE_MAP.get(str(market)))
        df = pd.read_csv(scv_file, dtype={"A股代码": "object"})
        for i in range(len(df)):
            code = df['A股代码'][i]
            name = df['A股简称'][i] if market == 1 else df['证券简称'][i]
            date = df['上市日期'][i] if market == 1 else datetime.strptime(str(df['上市日期'][i]),
                                                                       "%Y%m%d").strftime('%Y-%m-%d')
            date = datetime.strptime(date, "%Y-%m-%d").date()
            # 如果数据库中没有这条A股代码，就添加
            record = TABLE_MAP.get(str(market)).objects.filter(code__exact=code)
            if len(record) == 0:
                TABLE_MAP.get(str(market)).objects.create(code=code, name=name, date=date)

        result = {'data': {}, 'code': '200', 'message': '更新成功!'}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 删除一条股票记录(深市/沪市)
def deleteStockRecord(request):
    TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')
        if market not in [0, 1]:
            result = {'data': {}, 'code': '201', 'message': '删除失败，参数未指定深市or沪市!'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        stock_id = json_param.get('id')
        if not stock_id:
            result = {'data': {}, 'code': '202', 'message': '删除失败，参数未指定将删除股票的ID!'}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
        # 通过id删除数据库中的记录
        TABLE_MAP.get(str(market)).objects.filter(id__exact=stock_id).delete()
        result = {'data': {}, 'code': '200', 'message': '删除成功!'}
        # return JsonResponse(data=result) # 这种方式返回简单，但是message中文会乱码，所以改成HttpResponse来返回json数据
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
