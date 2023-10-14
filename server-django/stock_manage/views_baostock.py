import re
import json
import time
import datetime
import pandas as pd
import baostock as bs
from django.db import connection
from stock_manage import models_sql
from django.http.response import JsonResponse
from stock_manage.models import StockListSZ, StockListSH


# 更新股票历史数据
def update_history_data(request):
    if request.method == 'POST':
        post_body = request.body
        json_param = json.loads(post_body.decode())
        market = json_param.get('market')
        stock_code = json_param.get('code')
        release_date = json_param.get('release_date')
        code = f'SZ.{stock_code}' if str(market) == '1' else f'SH.{stock_code}'

        # 更新股票列表的状态（status: true更新中）
        if str(market) == '1':
            record = StockListSZ.objects.filter(code=stock_code).first()
            if record.status:
                return JsonResponse({'data': {}, 'code': '201', 'message': f'该股票code={code}正在更新中...'})
            StockListSZ.objects.filter(code=stock_code).update(status=True, update_time=datetime.datetime.now().date())
        else:
            record = StockListSH.objects.filter(code=stock_code).first()
            if record.status:
                return JsonResponse({'data': {}, 'code': '201', 'message': f'该股票code={code}正在更新中...'})
            StockListSH.objects.filter(code=stock_code).update(status=True, update_time=datetime.datetime.now().date())
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
            start_date = last_date[0][0].strftime('%Y-%m-%d') if last_date is not None and last_date[0][0] is not None else release_date
            # 获取数据入库的结束日期(当天)
            end_date = datetime.datetime.now().date()
            end_date = end_date.strftime("%Y-%m-%d")
            # 登陆证券宝系统
            bs.login()
            # 获取历史数据
            fields = "date, code, open, high, low, close, preclose, volume, amount, adjustflag, turn, tradestatus, " \
                     "pctChg, peTTM, pbMRQ, psTTM, pcfNcfTTM, isST"
            print('获取历史数据的参数：', f'market={market}', f'code={code}', f'start_date={start_date}', f'end_date={end_date}')
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
                if data[0][0] == 0:
                    # 增加历史数据sql
                    sql = f'{models_sql.INSERT_INTO_HISTORY_DATA}'.format(
                        TABLE_NAME=f'tb_{stock_code}',
                        date=row['date'],
                        code=re.findall(r'\d+\.?\d*', row['code'])[0],
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
                else:
                    # 更新历史数据sql
                    sql = f'{models_sql.UPDATE_HISTORY_DATA}'.format(
                        TABLE_NAME=f'tb_{stock_code}',
                        date=row['date'],
                        code=re.findall(r'\d+\.?\d*', row['code'])[0],
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
        finally:
            # 更新股票列表的状态（status: False） and 更新股票列表的更新时间（update_time）
            if str(market) == '1':
                StockListSZ.objects.filter(code=stock_code).update(
                    update_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()), status=False)
            else:
                StockListSH.objects.filter(code=stock_code).update(
                    update_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()), status=False)

    return JsonResponse({'data': data_list, 'code': '200', 'message': '更新成功!!'})


# 更新股票历史数据(深市股票all)
def update_history_data_sz(request):
    if request.method == 'POST':
        records = StockListSZ.objects.all()
        num = 0
        for record in records:
            num += 1
            if num not in range(150, 200):
                print('num=', num)
                continue
            if record.status:
                continue
            try:
                # 更新股票列表的状态（status: true更新中）
                StockListSZ.objects.filter(code=record.code).update(status=True)
                # 如果数据库表不存在，则创建
                sql = f'{models_sql.CREATE_TABLE_HISTORY_DATA}'.format(TABLE_NAME=f'tb_{record.code}')
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                # 获取数据入库的开始日期(数据库中最近的1条记录时间)
                sql = f'{models_sql.SELECT_MAX_DATE}'.format(TABLE_NAME=f'tb_{record.code}')
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    last_date = cursor.fetchall()
                start_date = last_date[0][0] if last_date is not None and last_date[0][0] is not None else record.date
                start_date = str(start_date)
                # 获取数据入库的结束日期(当天)
                end_date = datetime.datetime.now().date()
                end_date = end_date.strftime("%Y-%m-%d")
                # 登陆证券宝系统
                bs.login()
                # 获取历史数据
                fields = "date, code, open, high, low, close, preclose, volume, amount, adjustflag, turn," \
                         "tradestatus, pctChg, peTTM, pbMRQ, psTTM, pcfNcfTTM, isST"
                print('获取历史数据的参数：', f'code=SZ.{record.code}', f'start_date={start_date}', f'end_date={end_date}')
                respond = bs.query_history_k_data(code=f'SZ.{record.code}',
                                                  fields=fields,
                                                  start_date=start_date,
                                                  end_date=end_date)
                data_list = []
                while (respond.error_code == '0') & respond.next():  # 获取一条记录，将记录合并在一起
                    data_list.append(respond.get_row_data())
                result = pd.DataFrame(data_list, columns=respond.fields)
                # 将历史数据更新到数据库
                for index, row in result.iterrows():
                    # 判断row['date']日期的数据是否已存在（存在：更新/不存在：添加）
                    sql = f'{models_sql.SELECT_DATA_WHERE_DATE}'.format(TABLE_NAME=f'tb_{record.code}',
                                                                        date=row['date'])
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        data = cursor.fetchall()
                    if data[0][0] == 0:
                        # 增加历史数据sql
                        sql = f'{models_sql.INSERT_INTO_HISTORY_DATA}'.format(
                            TABLE_NAME=f'tb_{record.code}',
                            date=row['date'],
                            code=re.findall(r'\d+\.?\d*', row['code'])[0],
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
                    else:
                        # 更新历史数据sql
                        sql = f'{models_sql.UPDATE_HISTORY_DATA}'.format(
                            TABLE_NAME=f'tb_{record.code}',
                            date=row['date'],
                            code=re.findall(r'\d+\.?\d*', row['code'])[0],
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
            finally:
                # 更新股票列表的状态（status: False） and 更新股票列表的更新时间（update_time）
                StockListSZ.objects.filter(code=record.code).update(
                    update_time=time.strftime("%Y-%m-%d %H:%M", time.localtime()), status=False)

    return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})
