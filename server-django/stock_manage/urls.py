from django.urls import include, path
from stock_manage import views


urlpatterns = [
    path('getStockList/', views.getStockList),
    path('updateStockList/', views.updateStockList),
]
