import datetime
from django.db import models


# Create your models here.
class StockListSZ(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    today_date = models.DateField(default=None, verbose_name='今日行情日期')
    open = models.FloatField(default=0, verbose_name='今日开盘价')
    high = models.FloatField(default=0, verbose_name='最高价')
    low = models.FloatField(default=0, verbose_name='最低价')
    close = models.FloatField(default=0, verbose_name='今日收盘价')
    pre_close = models.FloatField(default=0, verbose_name='昨日收盘价')
    ratio = models.FloatField(default=0, verbose_name='涨跌幅')
    trade_status = models.IntegerField(default=1, verbose_name='交易状态')
    status = models.IntegerField(default=0, verbose_name='更新状态')
    slope = models.FloatField(default=0, verbose_name='斜率')
    intercept = models.FloatField(default=0, verbose_name='截距')
    trend_status = models.CharField(max_length=50, default=None, verbose_name='斜率状态')
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sz'
        # 为这个类定义一个说明
        verbose_name = '股票列表(深市)'
        # 不加这个的话在我们的verbose_name在admin里面会被自动加上s
        verbose_name_plural = '股票列表(深市)'


class StockListSH(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    today_date = models.DateField(default=None, verbose_name='今日行情日期')
    open = models.FloatField(default=0, verbose_name='今日开盘价')
    high = models.FloatField(default=0, verbose_name='最高价')
    low = models.FloatField(default=0, verbose_name='最低价')
    close = models.FloatField(default=0, verbose_name='今日收盘价')
    pre_close = models.FloatField(default=0, verbose_name='昨日收盘价')
    ratio = models.FloatField(default=0, verbose_name='涨跌幅')
    trade_status = models.IntegerField(default=1, verbose_name='交易状态')
    status = models.BooleanField(default=True, verbose_name='更新状态')
    slope = models.FloatField(default=0, verbose_name='斜率')
    intercept = models.FloatField(default=0, verbose_name='截距')
    trend_status = models.CharField(max_length=50, default=None, verbose_name='斜率状态')
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sh'
        verbose_name = '股票列表(沪市)'
        verbose_name_plural = '股票列表(沪市)'
