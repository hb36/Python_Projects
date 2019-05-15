# encoding:utf-8
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import markdown

from .models import Post, Category, Tag
from comments.forms import CommentForm


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
    # form = CommentForm()
    # comment_list = post.comment_set_all()
    context = {
        'post': post,
        # 'form': form,
        # 'comment_list': comment_list,
    }
    return render(request, 'blog/test.html', context)


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    ).order_by('-created_time')
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag).order_by('-created_time')
    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)
