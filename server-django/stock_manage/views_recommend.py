import json
from django.http import HttpResponse
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
            stockList = list(queryset)
            # 遍历股票列表
            for row in stockList:
                code = row['code']
                # 获取原始数据
                rawData = handler.getRawDataList(code, COUNT)
                if len(rawData) > 0:
                    # 分割原始数据 如:[[日期(date), 开盘(open)，收盘(close)，最低(low)，最高(high)]]，并倒序(日期从小到大)
                    data = [[element[0], element[1], element[2], element[3], element[4]] for element in rawData][::-1]

                    # ---------------计算MACD指标 start---------------
                    macd_data, dif_data, dea_data = macd.calculateMACD(10, 21, 9, data, 2)
                    print('macd_data=', macd_data)
                    print('dif_data=', dif_data)
                    print('dea_data=', dea_data)
                    # ---------------计算MACD指标 end-----------------

                # test code
                break
        return HttpResponse(json.dumps([], ensure_ascii=False), content_type="application/json,charset=utf-8")

