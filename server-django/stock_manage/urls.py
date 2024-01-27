from django.urls import include, path
from stock_manage import views, views_baostock, views_trend, views_stock_select


urlpatterns = [
    path('getStockList/', views.getStockList),
    path('getRawDataList/', views.getRawDataList),
    path('getRawDataDict/', views.getRawDataDict),
    path('updateStockList/', views.updateStockList),
    path('updateStatus/', views.updateStatus),
    path('deleteStockRecord/', views.deleteStockRecord),
    # baoStock
    path('update_history_data_single/', views_baostock.update_history_data_single),
    path('update_history_data_all/', views_baostock.update_history_data_all),
    # trend
    path('getUpTrendDataList/', views_trend.getUpTrendDataList),
    path('postUpdateTrendStatus/', views_trend.postUpdateTrendStatus),
    # stock select
    path('postUpdateStockSelect/', views_stock_select.postUpdateStockSelect),
]
