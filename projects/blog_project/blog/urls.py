# encoding:utf-8
from django.urls import path, re_path

from . import views

app_name = 'blog'
urlpatterns = [
    path('index/', views.index, name='index'),
    # path('post/<int:pk>/', views.detail, name='detail'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    re_path(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    re_path(r'^category/(?P<pk>[0-9]+)/$', views.category, name='category'),
    re_path(r'^tags/(?P<pk>[0-9]+)/$', views.tags, name='tags'),
    path('', views.hello),
]
