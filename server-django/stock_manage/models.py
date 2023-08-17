from django.db import models


# Create your models here.
class StockList(models.Model):
    name = models.CharField(max_length=32)
    code = models.CharField(max_length=32)
    create_time = models.CharField(max_length=32)
