# encoding:utf-8
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.hello),
    path('time/', views.time)
]
