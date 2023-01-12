from django.urls import include
from django.urls import re_path as url
from django.urls import path, reverse
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'donutapp/index.html'), name='index'),
    path('main/', lambda request: render(request, 'donutapp/main.html'), name='main'),
    path('profile/', lambda request: render(request, 'donutapp/profile.html'), name='profile'),
    path('statistics/', lambda request: render(request, 'donutapp/statistics.html'), name='statistics'),
]
