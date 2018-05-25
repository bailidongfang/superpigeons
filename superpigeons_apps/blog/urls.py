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
from .views import blog_index, blog_edit, blog_article, blog_comment, tags_edit

urlpatterns = [
    url(r'^$', blog_index, name='blog'),
    url(r'article/(?P<artid>.*)', blog_article, name='article'),
    url(r'comment/', blog_comment, name='comment'),
    url(r'blog_edit/(?P<ftype>.*)/(?P<artid>.*)', blog_edit, name='blogedit'),
    url(r'tags_edit/', tags_edit, name='tagsedit'),
]
