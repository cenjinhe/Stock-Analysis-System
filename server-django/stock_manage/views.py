from django.http.response import JsonResponse


# 获取股票列表信息
def getStockList(request):
    print('request.method=', request.method)
    if request.method == 'GET':
        jsondata = {
            'list': [
                {"code": "0001", "name": "金河生物", "date": "2023", "update_time": "2023"},
                {"code": "0002", "name": "银河生物", "date": "2023", "update_time": "2023"}
             ],
            'total': 2
        }
        # 返回前端json
        return JsonResponse({'data': jsondata, 'code': '200', 'message': '获取成功!'})


# 更新股票列表信息
def updateStockList(request):
    print('request.method=', request.method)
    pass
