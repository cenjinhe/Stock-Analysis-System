from django.shortcuts import render
from django.http import HttpResponse


def searchUser(request):
    name = request.GET.get('name')
    return HttpResponse("user" + name)
