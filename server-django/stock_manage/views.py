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
        trade_status = request.GET.get('trade_status', default=3)
        status = request.GET.get('status', default=2)
        market = request.GET.get('market', default='1')

        listData = []
        # 更新状态为(更新中or已更新)的记录
        if str(status) in ['0', '1']:
            # 交易状态为(0停牌or1正常or2退市)的记录
            if str(trade_status) in ['0', '1', '2']:
                records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                               name__contains=name,
                                                               trade_status__contains=trade_status,
                                                               status__contains=status).order_by('code')
            else:
                records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                               name__contains=name,
                                                               status__contains=status).order_by('code')
        else:
            # 更新状态为(全部)的记录&&交易状态为(0停牌or1正常or2退市)的记录
            if str(trade_status) in ['0', '1', '2']:
                records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                               trade_status__contains=trade_status,
                                                               name__contains=name).order_by('code')
            else:
                records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                               name__contains=name).order_by('code')
        # 分页
        try:
            page_info = Paginator(records, size).page(number=current)
        except Exception as ex:
            print(ex)
            return JsonResponse({'data': {}, 'code': '200', 'message': 'No data'})

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
                             "listing_date": record.date,
                             "date": last_data[0][1] if last_data else None,
                             "close": last_data[0][6] if last_data else None,
                             "pre_close": last_data[0][7] if last_data else None,
                             "trade_status": record.trade_status,
                             "status": record.status,
                             "update_time": record.update_time.strftime("%Y-%m-%d %H:%M:%S")})
        json_data = {'list': listData, 'total': len(records)}
        return JsonResponse({'data': json_data, 'code': '200', 'message': '获取成功!'})


# 获取股票状态列表
def getStatusList(request):
    TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
    if request.method == 'GET':
        size = request.GET.get('size', default=10)
        current = request.GET.get('current', default=1)
        code = request.GET.get('code', default='')
        name = request.GET.get('name', default='')
        status = request.GET.get('status', default=1)
        market = request.GET.get('market', default='1')

        listData = []
        if str(status) in ['0', '1']:
            records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                           name__contains=name,
                                                           status__contains=status).order_by('code')
        else:
            records = TABLE_MAP.get(market).objects.filter(code__contains=code,
                                                           name__contains=name).order_by('code')
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
            # 加入到数据列表中
            listData.append(record.status)
        return JsonResponse({'data': listData, 'code': '200', 'message': '获取成功!'})


# 获取原始数据列表
def getRawDataList(request):
    if request.method == 'GET':
        count = request.GET.get('count', default=100)
        code = request.GET.get('code', default='')

        sql = f'{models_sql.SELECT_RAW_DATA}'.format(TABLE_NAME=f'tb_{code}')
        with connection.cursor() as cursor:
            cursor.execute(sql)
            rawData = cursor.fetchall()

        return JsonResponse({'rawData': rawData, 'code': '200', 'message': '获取成功!'})


# 更新所有股票名称一览
def updateStockList(request):
    TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
    FILE_MAP = {'0': 'shA股列表.xlsx', '1': 'szA股列表.xlsx'}
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # scv_file = os.path.join(BASE_DIR, 'stock_manage', 'data', FILE_MAP.get(str(market)))
        # df = pd.read_csv(scv_file, dtype={"A股代码": "object"})
        file = os.path.join(BASE_DIR, 'stock_manage', 'data', FILE_MAP.get(str(market)))
        df = pd.read_excel(file, dtype={"A股代码": "object"})
        # update 所有股票名称一览
        for i in range(len(df)):
            code = df['A股代码'][i]
            name = df['A股简称'][i] if market == 1 else df['证券简称'][i]
            date = df['A股上市日期'][i] if market == 1 else datetime.strptime(str(df['A股上市日期'][i]),
                                                                         "%Y%m%d").strftime('%Y-%m-%d')
            date = datetime.strptime(date, "%Y-%m-%d").date()
            # 如果数据库中没有这条A股代码，就添加
            record = TABLE_MAP.get(str(market)).objects.filter(code__exact=code)
            if len(record) == 0:
                print(f'code={code}', f'name={name}', f'date={date}')
                TABLE_MAP.get(str(market)).objects.create(code=code, name=name, date=date)
            else:
                print(f'code={code}', f'name={name}')
                TABLE_MAP.get(str(market)).objects.filter(code=code).update(name=name)

        # update 退市股票的状态，不在A股列表中的code即为退市股票，交易状态设置为2（退市）
        codes = df['A股代码'].tolist()
        record_codes = list(TABLE_MAP.get(str(market)).objects.values_list('code', flat=True))
        if codes and record_codes:
            for record_code in record_codes:
                if record_code not in codes:
                    TABLE_MAP.get(str(market)).objects.filter(code=record_code).update(trade_status=2)

        result = {'data': {}, 'code': '200', 'message': '更新成功!'}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 切换状态
def updateStatus(request):
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')
        stock_code = json_param.get('code')

        # 切换状态
        if str(market) == '1':
            record = StockListSZ.objects.filter(code=stock_code).first()
            StockListSZ.objects.filter(code=stock_code).update(status=not record.status)
        else:
            record = StockListSH.objects.filter(code=stock_code).first()
            StockListSH.objects.filter(code=stock_code).update(status=not record.status)

        result = {'data': {}, 'code': '200', 'message': '切换成功!'}
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
        # 删除历史数据的表
        record = StockListSZ.objects.filter(id=stock_id).first()
        sql = f'{models_sql.DROP_TABLE}'.format(TABLE_NAME=f'tb_{record.code}')
        print('sql = ', sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
        # 通过id删除数据库中股票名称记录
        TABLE_MAP.get(str(market)).objects.filter(id__exact=stock_id).delete()

        result = {'data': {}, 'code': '200', 'message': '删除成功!'}
        # return JsonResponse(data=result) # 这种方式返回简单，但是message中文会乱码，所以改成HttpResponse来返回json数据
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
