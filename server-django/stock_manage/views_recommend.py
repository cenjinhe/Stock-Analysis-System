from django.http.response import JsonResponse
from django.core.paginator import Paginator
from stock_manage.utils import handler, 拟合斜率, MACD, MA
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
COUNT = 200

"""
只存储macd上升的股票
"""


# get股票推荐分析结果
def getStockRecommendResults(request):
    if request.method == 'GET':
        size = request.GET.get('size', default=10)
        current = request.GET.get('current', default=1)
        code = request.GET.get('code', default='')
        name = request.GET.get('name', default='')
        sortFieldName = request.GET.get('column', default='')
        order = request.GET.get('order', default='ascending')

        # 获取排序的字段名称和排序类型
        sortFieldName = 'code' if sortFieldName == '' else sortFieldName
        sortFieldName = sortFieldName if order == 'ascending' else '-' + sortFieldName

        # 查询
        records = StockOnAnalysis.objects.filter(code__contains=code, name__contains=name).order_by(sortFieldName)

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
                             "code": record.code,
                             "name": record.name,
                             "market": record.market,
                             "close": record.close,
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
        index = 1
        # 遍历[深市, 沪市]
        for market in [1]:
            # 分别获取[深市, 沪市]的股票列表
            queryset = TABLE_MAP.get(str(market)).objects.all().values()
            stockList = list(queryset)
            # 遍历股票列表
            for row in stockList:
                code = row['code']
                name = row['name']
                close = row['close']
                # 定义一个变量，用于存储个股的解析结果
                result = {'code': code, 'name': name, 'market': market, 'close': close}
                # 获取原始数据
                rawData = handler.getRawDataList(code, COUNT)
                if len(rawData) <= 2:
                    continue

                # 分割原始数据 如:[[日期(date), 开盘(open)，收盘(close)，最低(low)，最高(high)]]，并倒序(日期从小到大)
                data = [[element[0], element[1], element[2], element[3], element[4]] for element in rawData][::-1]

                # ---------------计算MACD指标 start---------------
                macd_data, dif_data, dea_data = MACD.calculateMACD(10, 21, 9, data, 2)
                lenght = len(macd_data)
                result['previous_macd'] = macd_data[lenght-2]
                result['current_macd'] = macd_data[lenght-1]
                # 判断 => 只解析macd上升的股票
                if float(result['current_macd']) < float(result['previous_macd']):
                    continue
                result['previous_dif'] = dif_data[lenght-2]
                result['current_dif'] = dif_data[lenght-1]
                result['previous_dea'] = dea_data[lenght-2]
                result['current_dea'] = dea_data[lenght-1]
                # ---------------计算MACD指标 end-----------------

                # ---------------计算MA 3日均线 start-------------
                ma_3_data = MA.calculateMA(3, data, 2)
                result['previous_ma_3'] = ma_3_data[lenght-2]
                result['current_ma_3'] = ma_3_data[lenght-1]
                # ---------------计算MA 3日均线 end---------------

                # ---------------计算MA 5日均线 start-------------
                ma_5_data = MA.calculateMA(5, data, 2)
                result['previous_ma_5'] = ma_5_data[lenght-2]
                result['current_ma_5'] = ma_5_data[lenght-1]
                # ---------------计算MA 5日均线 end---------------

                # ---------------计算 MACD的拟合斜率 start-----------
                # num件，计算趋势and斜率
                num = 3
                trend_data = 拟合斜率.getSlopeAndTrendByData(macd_data[-num:], 0)
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
                    code=result['code'],
                    name=result['name'],
                    market=result['market'],
                    close=result['close'],
                    previous_macd=result['previous_macd'],
                    current_macd=result['current_macd'],
                    previous_dif=result['previous_dif'],
                    current_dif=result['current_dif'],
                    previous_dea=result['previous_dea'],
                    current_dea=result['current_dea'],
                    previous_ma_3=result['previous_ma_3'],
                    current_ma_3=result['current_ma_3'],
                    previous_ma_5=result['previous_ma_5'],
                    current_ma_5=result['current_ma_5']
                )
                # ---------------解析结果入库 end---------------
                # 解析下一个数据
                index += 1
                # 打印信息
                print('result=', result)

                # test code
                break
        return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})
