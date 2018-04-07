from django.shortcuts import render, redirect
from django.contrib import auth
from superpigeons_apps.user.forms import LoginForm
# Create your views here.


def login(request):
    if request.method == 'GET':
        context = dict()
        context['loginform'] = LoginForm()
        return render(request, 'login.html', context)
    if request.method == 'POST':
        context = dict()
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            formusername = loginform.cleaned_data.get("username")
            formpassword = loginform.cleaned_data.get("password")
            loginuser = auth.authenticate(username=formusername, password=formpassword)
            auth.login(request, loginuser)
            # 加积分 每日登陆=a 写文章=b 评论=c 点赞=d
            # lev = level(formusername)
            # lev.comput_level("a")
            return redirect('index')
        else:
            context['loginform'] = loginform
            return render(request, 'login.html', context)


def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('index')
