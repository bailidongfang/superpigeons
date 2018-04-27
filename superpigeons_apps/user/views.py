from django.shortcuts import render, redirect
from django.contrib import auth
from superpigeons_apps.user.forms import LoginForm, RegisterForm
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.models import Article
# Create your views here.


def user_my_info(request, username):
    userinfo = UserInfo.objects.get(username=username)
    context = dict()
    context['userinfo'] = userinfo
    context['user'] = request.user
    return render(request, 'user_info.html', context)


def user_index(request, username):
    userinfo = UserInfo.objects.get(username=username)
    article = Article.objects.filter(auther__username=username)
    context = dict()
    context['userinfo'] = userinfo
    context['article'] = article
    return render(request, 'user_index.html', context)


def user_login(request):
    if request.method == 'GET':
        context = dict()
        context['loginform'] = LoginForm()
        return render(request, 'user_login.html', context)
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
            return render(request, 'user_login.html', context)


def user_logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('index')


def user_register(request):
    if request.method == 'GET':
        context = dict()
        context['registerform'] = RegisterForm()
        return render(request, 'user_register.html', context)

