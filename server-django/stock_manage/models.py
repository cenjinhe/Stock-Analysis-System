import datetime
from django.db import models
from django.db import connection


# config
class StockConfig(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    name = models.CharField(max_length=50, default=None, verbose_name='name')
    value = models.CharField(max_length=5000, default=None, verbose_name='value')
    default = models.CharField(max_length=5000, default=None, verbose_name='default value')

    class Meta:
        db_table = 'stock_config'
        # 为这个类定义一个说明
        verbose_name = '股票配置'
        # 不加这个的话在我们的verbose_name在admin里面会被自动加上s
        verbose_name_plural = '股票配置'


class StockListSZ(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    today_date = models.DateField(default=None, null=True, verbose_name='今日行情日期')
    open = models.FloatField(default=0, null=True, verbose_name='今日开盘价')
    high = models.FloatField(default=0, null=True, verbose_name='最高价')
    low = models.FloatField(default=0, null=True, verbose_name='最低价')
    close = models.FloatField(default=0, null=True, verbose_name='今日收盘价')
    pre_close = models.FloatField(default=0, null=True, verbose_name='昨日收盘价')
    ratio = models.FloatField(default=0, null=True, verbose_name='涨跌幅')
    trade_status = models.IntegerField(default=1, null=True, verbose_name='交易状态')
    status = models.IntegerField(default=False, null=True, verbose_name='更新状态')
    slope = models.FloatField(default=0, null=True, verbose_name='斜率')
    intercept = models.FloatField(default=0, null=True, verbose_name='截距')
    pre_trend_status = models.CharField(max_length=50, default=None, null=True, verbose_name='前回斜率状态')
    trend_status = models.CharField(max_length=50, default=None, null=True, verbose_name='当前斜率状态')
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sz'
        verbose_name = '股票列表(深市)'
        verbose_name_plural = '股票列表(深市)'


class StockListSH(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    date = models.DateField(verbose_name='上市日期')
    today_date = models.DateField(default=None, null=True, verbose_name='今日行情日期')
    open = models.FloatField(default=0, null=True, verbose_name='今日开盘价')
    high = models.FloatField(default=0, null=True, verbose_name='最高价')
    low = models.FloatField(default=0, null=True, verbose_name='最低价')
    close = models.FloatField(default=0, null=True, verbose_name='今日收盘价')
    pre_close = models.FloatField(default=0, null=True, verbose_name='昨日收盘价')
    ratio = models.FloatField(default=0, null=True, verbose_name='涨跌幅')
    trade_status = models.IntegerField(default=1, null=True, verbose_name='交易状态')
    status = models.BooleanField(default=False, null=True, verbose_name='更新状态')
    slope = models.FloatField(default=0, null=True, verbose_name='斜率')
    intercept = models.FloatField(default=0, null=True, verbose_name='截距')
    pre_trend_status = models.CharField(max_length=50, default=None, null=True, verbose_name='前回斜率状态')
    trend_status = models.CharField(max_length=50, default=None, null=True, verbose_name='当前斜率状态')
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_list_sh'
        verbose_name = '股票列表(沪市)'
        verbose_name_plural = '股票列表(沪市)'


# 用于存储推荐股票信息
class StockOnAnalysis(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, verbose_name='ID')
    # 股票基本信息
    date = models.DateTimeField(default=datetime.datetime.now(), verbose_name="行情日期")
    code = models.CharField(max_length=50, verbose_name='A股代码')
    name = models.CharField(max_length=50, verbose_name='A股简称')
    market = models.IntegerField(default=1, verbose_name='1深市 0沪市')
    close = models.FloatField(default=0, null=True, verbose_name='今日收盘价')
    current_close = models.FloatField(default=0, null=True, verbose_name='当前收盘价')
    # MACD指标
    previous_macd = models.FloatField(default=0, null=True, verbose_name='前一天的MACD值')
    current_macd = models.FloatField(default=0, null=True, verbose_name='现在的MACD值')
    previous_macd_3 = models.FloatField(default=0, null=True, verbose_name='前一天的3日MACD值')
    current_macd_3 = models.FloatField(default=0, null=True, verbose_name='现在的3日MACD值')
    previous_macd_5 = models.FloatField(default=0, null=True, verbose_name='前一天的5日MACD值')
    current_macd_5 = models.FloatField(default=0, null=True, verbose_name='现在的5日MACD值')
    previous_dif = models.FloatField(default=0, null=True, verbose_name='前一天的DIF值')
    current_dif = models.FloatField(default=0, null=True, verbose_name='现在的DIF值')
    previous_dea = models.FloatField(default=0, null=True, verbose_name='前一天的DEA值')
    current_dea = models.FloatField(default=0, null=True, verbose_name='现在的DEA值')
    # MA指标
    previous_ma_3 = models.FloatField(default=0, null=True, verbose_name='前一天的3日MA均线')
    current_ma_3 = models.FloatField(default=0, null=True, verbose_name='现在的3日MA均线')
    previous_ma_5 = models.FloatField(default=0, null=True, verbose_name='前一天的5日MA均线')
    current_ma_5 = models.FloatField(default=0, null=True, verbose_name='现在的5日MA均线')
    # 更新时间
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")

    class Meta:
        db_table = 'stock_on_analysis'
        verbose_name = '股票分析结果'
        verbose_name_plural = '股票分析结果'

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            print(cls)
            cursor.execute('TRUNCATE TABLE {0}'.format('stock_on_analysis'))
