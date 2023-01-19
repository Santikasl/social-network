from django.urls import include
from django.urls import re_path as url
from django.urls import path, reverse
from .views import *
from django.shortcuts import render

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('signin/', SignIn.as_view(), name='signin'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('exit/', logout_user, name='exit'),
    path('main/', Main.as_view(), name='main'),
    path('profile/', UserProfile.as_view(), name='profile'),

    path('statistics/', lambda request: render(request, 'donutapp/statistics.html'), name='statistics'),
]
