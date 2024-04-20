#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2024/4/19 23:20
# @File     : 更新推荐股票.py

import os
import sys
import django
import argparse
import datetime
from multiprocessing import Process, Queue, cpu_count
# ‘/server-django’目录加到系统目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, os.path.pardir)))
# 子进程中import models之前需要重新配置django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis
from stock_manage.utils import handler, MACD, MA, StockConfig, 拟合斜率


TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
NUM_MACD = 200
NUM_TREND = 3


def worker(queue, checkedMACD, macdNum, trendNum, date, id=None):
    queue.get()

    index = 1
    # 遍历[深市, 沪市]
    for market in [1]:
        # 分别获取[深市, 沪市]的股票列表
        queryset = TABLE_MAP.get(str(market)).objects.all().values()
        stockList = list(queryset)
        # 遍历[深市, 沪市]股票列表
        for row in stockList:
            code = row['code']
            name = row['name']

            # 获取原始数据
            rawData = handler.getRawDataListFromEndDate(code, date, macdNum)
            if len(rawData) <= 2:
                continue

            # 定义一个变量result，用于存储个股的解析结果
            result = {'date': rawData[0][0], 'code': code, 'name': name, 'market': market,
                      'close': rawData[0][2]}
            print('解析：', result)

            # 分割原始数据 如:[[日期(date), 开盘(open)，收盘(close)，最低(low)，最高(high)]]，并倒序(日期从小到大)
            data = [[element[0], element[1], element[2], element[3], element[4]] for element in rawData][::-1]
            lenght = len(data)

            # ---------------计算MA 3日均线 start-------------
            ma_3_data = MA.calculateMA(3, data, 2)
            result['previous_ma_3'] = ma_3_data[lenght - 2]
            result['current_ma_3'] = ma_3_data[lenght - 1]
            # ---------------计算MA 3日均线 end---------------

            # ---------------计算MA 5日均线 start-------------
            ma_5_data = MA.calculateMA(5, data, 2)
            result['previous_ma_5'] = ma_5_data[lenght - 2]
            result['current_ma_5'] = ma_5_data[lenght - 1]
            # ---------------计算MA 5日均线 end---------------

            # ---------------计算MACD指标 start---------------
            if '1日' in checkedMACD:
                macd_data, dif_data, dea_data = MACD.calculateMACD(10, 21, 9, data, 2)
                result['previous_macd'] = macd_data[lenght - 2]
                result['current_macd'] = macd_data[lenght - 1]
                # 判断 => 只解析macd上升的股票
                if float(result['current_macd']) <= float(result['previous_macd']):
                    continue
                result['previous_dif'] = dif_data[lenght - 2]
                result['current_dif'] = dif_data[lenght - 1]
                result['previous_dea'] = dea_data[lenght - 2]
                result['current_dea'] = dea_data[lenght - 1]
            # ---------------计算MACD指标 end-----------------

            # ---------------计算3日均线的 MACD指标 start---------------
            if '3日' in checkedMACD:
                data_3 = list(map(MA.map_mcad_data, data, ma_3_data))
                macd_data_3, dif_data_3, dea_data_3 = MACD.calculateMACD(10, 21, 9, data_3, 2)
                result['previous_macd_3'] = macd_data_3[lenght - 2]
                result['current_macd_3'] = macd_data_3[lenght - 1]
                # 判断 => 只解析3日均线的 macd上升的股票
                if float(result['current_macd_3']) <= float(result['previous_macd_3']):
                    continue
                result['previous_dif_3'] = dif_data_3[lenght - 2]
                result['current_dif_3'] = dif_data_3[lenght - 1]
            # ---------------计算3日均线的 MACD指标 end-----------------

            # ---------------计算5日均线的 MACD指标 start---------------
            if '5日' in checkedMACD:
                data_5 = list(map(MA.map_mcad_data, data, ma_5_data))
                macd_data_5, dif_data_5, dea_data_5 = MACD.calculateMACD(10, 21, 9, data_5, 2)
                result['previous_macd_5'] = macd_data_5[lenght - 2]
                result['current_macd_5'] = macd_data_5[lenght - 1]
                # 判断 => 只解析5日均线的 macd上升的股票
                if float(result['current_macd_5']) <= float(result['previous_macd_5']):
                    continue
                result['previous_dif_5'] = dif_data_5[lenght - 2]
                result['current_dif_5'] = dif_data_5[lenght - 1]
            # ---------------计算5日均线的 MACD指标 end-----------------

            # ---------------计算7日均线的 MACD指标 start---------------
            if '7日' in checkedMACD:
                ma_7_data = MA.calculateMA(7, data, 2)
                data_7 = list(map(MA.map_mcad_data, data, ma_7_data))
                macd_data_7, dif_data_7, dea_data_7 = MACD.calculateMACD(10, 21, 9, data_7, 2)
                result['previous_macd_7'] = macd_data_7[lenght - 2]
                result['current_macd_7'] = macd_data_7[lenght - 1]
                # 判断 => 只解析7日均线的 macd上升的股票
                if float(result['current_macd_7']) <= float(result['previous_macd_7']):
                    continue
                result['previous_dif_7'] = dif_data_7[lenght - 2]
                result['current_dif_7'] = dif_data_7[lenght - 1]
            # ---------------计算7日均线的 MACD指标 end-----------------

            # ---------------计算14日均线的 MACD指标 start---------------
            if '14日' in checkedMACD:
                ma_14_data = MA.calculateMA(14, data, 2)
                data_14 = list(map(MA.map_mcad_data, data, ma_14_data))
                macd_data_14, dif_data_14, dea_data_14 = MACD.calculateMACD(10, 21, 9, data_14, 2)
                result['previous_macd_14'] = macd_data_14[lenght - 2]
                result['current_macd_14'] = macd_data_14[lenght - 1]
                # 判断 => 只解析14日均线的 macd上升的股票
                if float(result['current_macd_14']) <= float(result['previous_macd_14']):
                    continue
                result['previous_dif_14'] = dif_data_14[lenght - 2]
                result['current_dif_14'] = dif_data_14[lenght - 1]
            # ---------------计算14日均线的 MACD指标 end-----------------

            # ---------------计算20日均线的 MACD指标 start---------------
            if '20日' in checkedMACD:
                ma_20_data = MA.calculateMA(20, data, 2)
                data_20 = list(map(MA.map_mcad_data, data, ma_20_data))
                macd_data_20, dif_data_20, dea_data_20 = MACD.calculateMACD(10, 21, 9, data_20, 2)
                result['previous_macd_20'] = macd_data_20[lenght - 2]
                result['current_macd_20'] = macd_data_20[lenght - 1]
                # 判断 => 只解析20日均线的 macd上升的股票
                if float(result['current_macd_20']) <= float(result['previous_macd_20']):
                    continue
                result['previous_dif_20'] = dif_data_20[lenght - 2]
                result['current_dif_20'] = dif_data_20[lenght - 1]
            # ---------------计算20日均线的 MACD指标 end-----------------

            # ---------------计算30日均线的 MACD指标 start---------------
            if '30日' in checkedMACD:
                ma_30_data = MA.calculateMA(30, data, 2)
                data_30 = list(map(MA.map_mcad_data, data, ma_30_data))
                macd_data_30, dif_data_30, dea_data_30 = MACD.calculateMACD(10, 21, 9, data_30, 2)
                result['previous_macd_30'] = macd_data_30[lenght - 2]
                result['current_macd_30'] = macd_data_30[lenght - 1]
                # 判断 => 只解析30日均线的 macd上升的股票
                if float(result['current_macd_30']) <= float(result['previous_macd_30']):
                    continue
                result['previous_dif_30'] = dif_data_30[lenght - 2]
                result['current_dif_30'] = dif_data_30[lenght - 1]
            # ---------------计算30日均线的 MACD指标 end-----------------

            # ---------------计算 MACD的拟合斜率 start-----------
            # trendNum件，计算趋势and斜率
            macd_data, dif_data, dea_data = MACD.calculateMACD(10, 21, 9, data, 2)
            trend_data = 拟合斜率.getSlopeAndTrendByData(macd_data[-trendNum:], 0)
            result['slope'] = trend_data['slope']
            result['trend_status'] = trend_data['trend_status']
            # ---------------计算 拟合斜率 end-------------

            # ---------------解析结果入库 start-------------
            # 增加数据
            StockOnAnalysis.objects.create(
                id=index,
                date=result['date'],
                code=result['code'],
                name=result['name'],
                market=result['market'],
                close=result['close'],
                current_close=result['close'],
                # MACD
                previous_macd=result['previous_macd'] if 'previous_macd' in result else None,
                current_macd=result['current_macd'] if 'current_macd' in result else None,
                previous_macd_3=result['previous_macd_3'] if 'previous_macd_3' in result else None,
                current_macd_3=result['current_macd_3'] if 'current_macd_3' in result else None,
                previous_macd_5=result['previous_macd_5'] if 'previous_macd_5' in result else None,
                current_macd_5=result['current_macd_5'] if 'current_macd_5' in result else None,
                previous_dif=result['previous_dif'] if 'previous_dif' in result else None,
                current_dif=result['current_dif'] if 'current_dif' in result else None,
                previous_dea=result['previous_dea'] if 'previous_dea' in result else None,
                current_dea=result['current_dea'] if 'current_dea' in result else None,
                # MA
                previous_ma_3=result['previous_ma_3'] if 'previous_ma_3' in result else None,
                current_ma_3=result['current_ma_3'] if 'current_ma_3' in result else None,
                previous_ma_5=result['previous_ma_5'] if 'previous_ma_5' in result else None,
                current_ma_5=result['current_ma_5'] if 'current_ma_5' in result else None
            )
            # ---------------解析结果入库 end---------------
            # 解析下一个数据
            index += 1


def run_queue(checkedMACD, macdNum, trendNum, date):
    # 获取CPU核数
    # cpuCount = cpu_count()
    cpuCount = 1
    # 创建先进先出队列
    queue = Queue(maxsize=cpuCount)
    # 填充队列
    [queue.put(index) for index in range(cpuCount)]
    # 获取子进程的参数

    # 创建子进程
    process = [Process(target=worker, args=(queue,
                                            checkedMACD,
                                            macdNum,
                                            trendNum,
                                            date,
                                            index)) for index in range(cpuCount)]
    # 启动子进程
    [p.start() for p in process]
    # 等待所有子进程结束
    [p.join() for p in process]
    print('运行结束')


if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='更新推荐股票')
    parser.add_argument('--checkedMACD', type=str, nargs='+', default=['1日', '3日', '5日', '7日', '15日'], help='macd采集')
    parser.add_argument('--macdNum', type=int, default=200, help='计算macd数据的件数')
    parser.add_argument('--trendNum', type=int, default=3, help='计算拟合斜率数据的件数')
    parser.add_argument('--date', type=str, default=datetime.date.today(), help='行情日期')
    # 获取所有参数
    args = parser.parse_args()

    try:
        # 更新状态:updating
        StockConfig.setConfigValue(name='status_recommend', value='updating')
        # 清空数据库表
        StockOnAnalysis.objects.all().delete()
        # 运行队列
        run_queue(checkedMACD=args.checkedMACD, macdNum=args.macdNum, trendNum=args.trendNum, date=args.date)
    except Exception as ex:
        print(ex)
    finally:
        # 更新状态:completed
        StockConfig.setConfigValue(name='status_recommend', value='completed')
        pass
    print('end!!!!!!!!!!!!')
