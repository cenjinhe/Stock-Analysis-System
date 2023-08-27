import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class StockListSZ(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    update_time = models.DateTimeField(default=timezone.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sz'
        verbose_name = '股票列表(深市)'


class StockListSH(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    update_time = models.DateTimeField(default=timezone.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sh'
        verbose_name = '股票列表(沪市)'
