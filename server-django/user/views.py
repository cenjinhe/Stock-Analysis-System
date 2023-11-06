#!/usr/bin/python
# -*- coding: UTF-8 -*-
from django.http.response import JsonResponse, HttpResponse


def login(request):
    if request.method == 'POST':
        json_data = {'token': 'token', 'refresh_token': 'refresh_token'}
        return JsonResponse({'data': json_data, 'code': '200', 'message': '登录成功!'})


def userinfo(request):
    if request.method == 'GET':
        json_data = {'id': 1, 'name': '金河岑', 'role|1': ['admin', 'visitor'], 'avatar': "@image('48x48', '#fb0a2a')"}
        return JsonResponse({'data': json_data, 'code': '200', 'message': '获取用户信息成功'})


def menus(request):
    if request.method == 'GET':
        return JsonResponse({'data': [], 'code': '200', 'message': '获取菜单成功'})
