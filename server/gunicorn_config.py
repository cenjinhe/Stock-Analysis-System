#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/6/10 16:29
# @File     : gunicorn_config.py.py

import multiprocessing

bind = "0.0.0.0:5000"              # 绑定服务的IP和端口号
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2                        # 处理请求的进程数

# backlog:服务器中在pending状态的最大连接数，即client处于waiting的数目。
# 超过这个数目， client连接会得到一个error。建议值64-2048。
backlog = 2048
worker_class = "eventlet"          # 有 sync, eventlet(并发), gevent, tornado, gthread选项
worker_connections = 1000          # 客户端最大同时连接数。只适用于eventlet， gevent工作方式
daemon = True                      # 后台运行
pidfile = './log/gunicorn.pid'       # pid存储文件路径
accesslog = './log/access.log'       # 访问日志文件
errorlog = './log/gunicorn.log'      # 错误日志文件
