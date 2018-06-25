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
# from superpigeons import settings
from django.conf.urls import url, include
# from django.views.static import serve
from common.FromFtp import get_from_ftp
from django.contrib import admin
from superpigeons_apps.index.views import index



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'blog/', include('superpigeons_apps.blog.urls')),
    url(r'auth/', include('superpigeons_apps.user.urls')),
    url(r'^ckeditor/', include('other_apps.ckeditor_uploader.urls')),
    url(r'^media/(?P<path>.*)$', get_from_ftp),
]
