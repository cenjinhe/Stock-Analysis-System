#!/usr/bin/python
# -*- coding: UTF-8 -*-
import datetime
from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    password = models.CharField(max_length=32, verbose_name="密码")
    role = models.CharField(max_length=32, verbose_name="角色")   # 管理员Admin/普通用户Normal/访客Guest/）
    notes = models.CharField(max_length=200, verbose_name="备注")
    update_time = models.DateTimeField(default=datetime.datetime.now(), verbose_name="更新时间")
