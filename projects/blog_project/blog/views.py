# encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import datetime


def index(request):
    return render(request, 'index.html', context={
        'title': "我的博客",
        'welcome': "欢迎来到我的博客"
    })


def hello(request):
    return HttpResponse("hello")


def time(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>It is %s.</h1></body></html>" % now
    return HttpResponse(html)
