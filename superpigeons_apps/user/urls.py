"""superpigeons URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# import django_comments
from django.conf.urls import url
from .views import user_login, user_logout, user_index, user_my_info,user_register,user_my_info_headpic

urlpatterns = [
    url(r'login/', user_login, name='login'),
    url(r'logout/', user_logout, name='logout'),
    url(r'myinfo/(?P<username>.*)', user_my_info, name='myinfo'),
    url(r'myinfo_headpic/', user_my_info_headpic, name='myinfo_headpic'),
    url(r'userindex/(?P<username>.*)', user_index, name='userindex'),
    url(r'register/', user_register, name='userregister')
]
