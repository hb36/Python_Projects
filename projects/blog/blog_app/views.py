# encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html', context={
        'title': '我的博客首页',
        'welcome': '欢迎访问我的博客首页'
    })


def test(request):
    return HttpResponse("Test")
