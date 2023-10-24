from django.urls import include, path
from stock_manage import views
from stock_manage import views_baostock


urlpatterns = [
    path('getStockList/', views.getStockList),
    path('getStatusList/', views.getStatusList),
    path('getRawDataList/', views.getRawDataList),
    path('updateStockList/', views.updateStockList),
    path('updateStatus/', views.updateStatus),
    path('deleteStockRecord/', views.deleteStockRecord),
    path('update_history_data/', views_baostock.update_history_data),
    path('update_history_data_sz/', views_baostock.update_history_data_sz),
]
