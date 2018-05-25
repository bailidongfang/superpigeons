from django.http.response import HttpResponse
from superpigeons_apps.user.models import UserInfo
from django.shortcuts import render, redirect


def user_inter_permission(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        for i in kwargs:
            username = kwargs[i]
        if request.method == 'GET':
            if str(request.user) == username:
                return func(*args, **kwargs)
            else:
                return redirect('/')
        if request.method == 'POST':
            if str(request.user) == request.POST['permission_name']:
                return func(*args, **kwargs)
            else:
                return HttpResponse('permission denied')
    return wrapper


def article_inter_permission(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        artid = kwargs['artid']
        ftype = kwargs['ftype']
        if ftype == 'add':
            return func(*args, **kwargs)
        else:
            art_owner = UserInfo.objects.get(user__article__id=artid).username
            requester = request.user
            if str(art_owner) == str(requester):
                return func(*args, **kwargs)
            else:
                if request.method == 'POST':
                    return HttpResponse('permission denied')
                else:
                    return redirect('/')
    return wrapper
