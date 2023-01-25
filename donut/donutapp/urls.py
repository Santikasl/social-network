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
    path('follow/', Follow.as_view(), name='follow'),
    path('<int:pk>/', SearchProfile.as_view(), name='search_profile'),
    path('newpost/', NewPost.as_view(), name='newpost'),
    path('search/', Search.as_view(), name='search'),
    path('like/', Like.as_view(), name='like'),
    path('delite', delite, name='delite'),
    path('edit/', edit, name='edit'),
    path('statistics/', Statistics.as_view(), name='statistics'),

]
