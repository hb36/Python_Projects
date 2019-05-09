# encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown

from .models import Post


def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    context = {
        'post_list': post_list,
    }
    return render(request, 'blog/index.html', context)


def hello(request):
    return HttpResponse("Welcome to my blog !")


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    context = {
        'post': post,
    }
    return render(request, 'blog/detail.html', context)
