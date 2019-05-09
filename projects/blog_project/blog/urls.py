# encoding:utf-8
from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('post/<int:pk>/', views.detail, name='detail'),
    path('', views.hello),

]
