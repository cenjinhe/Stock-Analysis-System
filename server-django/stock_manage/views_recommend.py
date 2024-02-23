import json
from django.http import HttpResponse
from stock_manage.utils import handler, 拟合斜率, macd
from stock_manage.models import StockListSZ, StockListSH, StockOnAnalysis

TABLE_MAP = {'0': StockListSH, '1': StockListSZ}
COUNT = 200


# 更新股票推荐分析结果
def postUpdateStockRecommend(request):
    if request.method == 'POST':
        results = []
        # 遍历[深市, 沪市]
        for market in [1]:
            # 分别获取[深市, 沪市]的股票列表
            queryset = TABLE_MAP.get(str(market)).objects.all().values()
            stockList = list(queryset)
            # 遍历股票列表
            for row in stockList:
                code = row['code']
                name = row['name']
                # 定义一个变量，用于存储个股的解析结果
                result = {'code': code, 'name': name}
                # 获取原始数据
                rawData = handler.getRawDataList(code, COUNT)
                if len(rawData) <= 2:
                    continue

                # 分割原始数据 如:[[日期(date), 开盘(open)，收盘(close)，最低(low)，最高(high)]]，并倒序(日期从小到大)
                data = [[element[0], element[1], element[2], element[3], element[4]] for element in rawData][::-1]

                # ---------------计算MACD指标 start---------------
                macd_data, dif_data, dea_data = macd.calculateMACD(10, 21, 9, data, 2)
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
                # 判断 => 只解析 DIF > DEA 的股票
                if float(result['current_dif']) < float(result['current_dea']):
                    continue
                # ---------------计算MACD指标 end-----------------

                # ---------------计算MA 3日均线 start-------------
                # ---------------计算MA 3日均线 end---------------

                # ---------------计算MA 5日均线 start-------------
                # ---------------计算MA 5日均线 end---------------

                # ---------------存储个股的解析结果 start-----------
                results.append(result)
                # ---------------存储个股的解析结果 end-------------

                # test code
                # break
        # ---------------解析结果入库 start-------------
        for index in range(len(results)):
            print('index=', index, results[index])
        # ---------------解析结果入库 end---------------
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")

