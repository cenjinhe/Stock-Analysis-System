"""
Django models filter筛选条件详解: https://www.cnblogs.com/qq128/p/13428278.html
功能: 只存储macd上升的股票
"""
import json
import datetime
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from stock_manage.models import StockOnAnalysis
from stock_manage.utils import AsyncCall, handler

NUM_MACD = 200
NUM_TREND = 3


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
        numDay = request.GET.get('compareDate', default='0')
        stStock = request.GET.get('stStock', default=1)
        # 排序字段
        sortFieldName = request.GET.get('column', default='')
        order = request.GET.get('order', default='ascending')

        # 获取排序的字段名称和排序类型
        sortFieldName = 'code' if sortFieldName == '' else sortFieldName
        sortFieldName = sortFieldName if order == 'ascending' else '-' + sortFieldName

        # 查询条件为空值时的处理
        macdStart = -100 if not macdStart else macdStart
        macdEnd = 100 if not macdEnd else macdEnd

        # 查询 & 字段排序
        querySet = StockOnAnalysis.objects.filter(
            code__contains=code,
            name__contains=name,
            current_macd__range=(macdStart, macdEnd)
        ).order_by(sortFieldName)

        # 过滤ST股票
        if str(stStock) == '0':
            querySet = querySet.exclude(name__icontains='ST')

        # 分页
        try:
            page_info = Paginator(querySet, size).page(number=current)
        except Exception as ex:
            print(ex)
            return JsonResponse({'data': {}, 'code': '200', 'message': 'No data'})

        listData = []
        for record in page_info:
            # 获取对比日期的收盘价
            compare_date, compare_close = _queryCloseFromStartDate(record.code, record.date, numDay)
            # 加入到数据列表中
            listData.append({"id": record.id,
                             "date": record.date.strftime("%Y-%m-%d"),
                             "code": record.code,
                             "name": record.name,
                             "market": record.market,
                             "close": record.close,
                             "compare_close": compare_close,
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
                             "update_time": compare_date.strftime("%Y-%m-%d")})
        json_data = {'list': listData, 'total': len(querySet)}
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
            print('更新推荐股票参数：', checkedMACD, macdNum, trendNum, date)

            # 异步执行-更新推荐股票.py脚本
            file_path = 'stock_manage/utils/更新推荐股票.py'
            AsyncCall.async_call_file(file_path, {'checkedMACD': " ".join(str(i) for i in checkedMACD),
                                                  'macdNum': macdNum,
                                                  'trendNum': trendNum,
                                                  'date': date})
        except Exception as ex:
            print(ex)
        finally:
            pass
        return JsonResponse({'data': {}, 'code': '200', 'message': '更新成功!!'})


def _queryCloseFromStartDate(code, date, count):
    """获取对比日期的收盘价"""
    rawData = handler.getRawDataListFromStartDate(code, date, count)
    data = rawData[0]
    return data['date'], data['close']
