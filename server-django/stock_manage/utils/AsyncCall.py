#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2024/4/20 15:45
# @File     : async.py

import subprocess


def async_call_file(file_path, args=None):
    """ 异步调用另一个py文件 不阻塞 """
    # 获取参数
    process_args = f'python {file_path}'
    if args:
        for (key, value) in args.items():
            process_args += ' ' + f'--{key} {value}'

    print(f'异步调用另一个py文件: {process_args}')
    subprocess.Popen(process_args)
