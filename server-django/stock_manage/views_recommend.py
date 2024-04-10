"""
Django models filter筛选条件详解: https://www.cnblogs.com/qq128/p/13428278.html
"""
import json
import datetime
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from stock_manage.utils import handler, 拟合斜率, MACD, MA, StockConfig
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
NUM_MACD = 200
NUM_TREND = 3

"""
只存储macd上升的股票
"""


# get股票推荐分析结果
def getStockRecommendResults(request):
    if request.method == 'GET':
        # page页
        size = request.GET.get('size', default=10)
        current = request.GET.get('current', default=1)
        # 查询条件
        code = request.GET.get('code', default='')
        name = request.GET.get('name', default='')
        macdStart = request.GET.get('macdStart', default=-100)
        macdEnd = request.GET.get('macdEnd', default=100)
        # 排序字段
        sortFieldName = request.GET.get('column', default='')
        order = request.GET.get('order', default='ascending')

        # 获取排序的字段名称和排序类型
        sortFieldName = 'code' if sortFieldName == '' else sortFieldName
        sortFieldName = sortFieldName if order == 'ascending' else '-' + sortFieldName

        # 查询条件为空值时的处理
        macdStart = -100 if not macdStart else macdStart
        macdEnd = 100 if not macdEnd else macdEnd

        # 查询
        records = StockOnAnalysis.objects.filter(
            code__contains=code,
            name__contains=name,
            current_macd__range=(macdStart, macdEnd)
            ).order_by(sortFieldName)

        # 分页
        try:
            page_info = Paginator(records, size).page(number=current)
        except Exception as ex:
            print(ex)
            return JsonResponse({'data': {}, 'code': '200', 'message': 'No data'})

        listData = []
        for record in page_info:
            # 加入到数据列表中
            listData.append({"id": record.id,
                             "date": record.date.strftime("%Y-%m-%d"),
                             "code": record.code,
                             "name": record.name,
                             "market": record.market,
                             "close": record.close,
                             "current_close": record.current_close,
                             "previous_macd": record.previous_macd,
                             "current_macd": record.current_macd,
                             "previous_dif": record.previous_dif,
                             "current_dif": record.current_dif,
                             "previous_dea": record.previous_dea,
                             "current_dea": record.current_dea,
                             "previous_ma_3": record.previous_ma_3,
                             "current_ma_3": record.current_ma_3,
                             "previous_ma_5": record.previous_ma_5,
                             "current_ma_5": record.current_ma_5,
                             "update_time": record.update_time.strftime("%Y-%m-%d %H:%M:%S")})
        json_data = {'list': listData, 'total': len(records)}
        return JsonResponse({'data': json_data, 'code': '200', 'message': '获取成功!'})


# update股票推荐分析结果
def postUpdateStockRecommend(request):
    if request.method == 'POST':
        try:
            # 解析参数
            post_body = request.body
            json_param = json.loads(post_body.decode())
            checkedMACD = json_param.get('checkedMACD', [])
            macdNum = json_param.get('macdNum', NUM_MACD)
            trendNum = json_param.get('trendNum', NUM_TREND)
            date = json_param.get('date', datetime.date.today())
            if not date:
                date = datetime.date.today()
            print(checkedMACD, macdNum, trendNum, date)

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
                    rawData = handler.getRawDataListFromDate(code, date, macdNum)
                    if len(rawData) <= 2:
                        continue

                    # 定义一个变量result，用于存储个股的解析结果
                    result = {'date': rawData[0][0], 'code': code, 'name': name, 'market': market, 'close': rawData[0][2]}
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
                        data_3 = list(map(map_mcad_data, data, ma_3_data))
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
                        data_5 = list(map(map_mcad_data, data, ma_5_data))
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
                        data_7 = list(map(map_mcad_data, data, ma_7_data))
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
                        data_14 = list(map(map_mcad_data, data, ma_14_data))
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
                        data_20 = list(map(map_mcad_data, data, ma_20_data))
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
                        data_30 = list(map(map_mcad_data, data, ma_30_data))
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
                    # 删除表所有数据
                    if index == 1:
                        StockOnAnalysis.objects.all().delete()
                    # 重新插入新数据
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

                    # test code
                    # break
        except Exception as ex:
            print(ex)
        finally:
            # 更新状态
            StockConfig.setConfigValue(name='status_recommend', value='completed')
        return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})


# 更新当前收盘价
def postUpdateCurrentClose(request):
    if request.method == 'POST':
        try:
            queryset = StockOnAnalysis.objects.all().values()
            stockList = list(queryset)
            # 遍历列表
            for row in stockList:
                code = row['code']
                name = row['name']
                # 获取当前收盘价
                for market in [1, 0]:
                    record = TABLE_MAP.get(str(market)).objects.filter(code=code, name=name).first()
                    if not record:
                        continue
                    # 更新当前收盘价
                    StockOnAnalysis.objects.filter(code=code, name=name).update(current_close=record.close,
                                                                                update_time=datetime.datetime.now())
        except Exception as ex:
            print(ex)
        finally:
            # 更新状态
            StockConfig.setConfigValue(name='status_recommend', value='completed')
        return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})


def map_mcad_data(x, y):
    """将MA数据转换为MACD数据"""
    if y == '-':
        y = 0
    x[2] = float(y)
    return x
