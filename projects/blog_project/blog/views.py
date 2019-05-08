# encoding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import datetime

from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def hello(request):
    return HttpResponse("Welcome to my blog !")


def time(request):
    now = datetime.datetime.now()
    html = "<html><body><h1>It is %s.</h1></body></html>" % now
    return HttpResponse(html)
