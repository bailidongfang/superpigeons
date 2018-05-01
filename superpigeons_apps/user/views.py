from django.shortcuts import render, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from superpigeons_apps.user.forms import LoginForm, RegisterForm
from superpigeons_apps.user.models import UserInfo
from superpigeons_apps.blog.models import Article
from common.FromFtp import upload_to_ftp
from django.db import transaction
from PIL import Image
import os
from superpigeons import settings
# Create your views here.


def user_my_info(request, username):
    userinfo = UserInfo.objects.get(username=username)
    context = dict()
    context['userinfo'] = userinfo
    context['user'] = request.user
    return render(request, 'user_info.html', context)


def user_my_info_headpic(request):
    # 剪裁数据获取
    username = request.POST['user']
    file = request.FILES['avatar_file']
    top = int(float(request.POST['avatar_y']))
    buttom = top + int(float(request.POST['avatar_height']))
    left = int(float(request.POST['avatar_x']))
    right = left + int(float(request.POST['avatar_width']))
    # 打开图片
    im = Image.open(file)
    # 剪裁图片
    crop_im = im.crop((left, top, right, buttom))
    # 保存图片
    crop_im.save(os.path.join(settings.BASE_DIR, "tmp.jpg"))

    # with open(os.path.join(settings.BASE_DIR, "tmp.jpg"), 'wb') as f:
    #     upload_to_ftp(f)

    # userinfo = UserInfo.objects.get(username=username)
    # userinfo.headpic = memfile
    # userinfo.save()
    return HttpResponse("ok")


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
    if request.method == 'POST':
        registerform = RegisterForm(request.POST)
        context = dict()
        if registerform.is_valid():
            # 提取form数据
            formusername = registerform.cleaned_data.get("username")
            formpassword = registerform.cleaned_data.get("password")
            formemail = registerform.cleaned_data.get("useremail")
            context['registerform'] = registerform
            # 用户数据入库
            try:
                # 两条数据绑定在同一个事务上，保证数据一致
                with transaction.atomic():
                    newuser = User.objects.create_user(username=formusername, password=formpassword, email=formemail)
                    UserInfo.objects.create(user=newuser, username=formusername, nickname=formusername)
            except Exception as e:
                print(e)
                context['message'] = 'error'
                return render(request, 'user_register.html', context)
            else:
                context['message'] = 'success'
                return render(request, 'user_register.html', context)
        else:
            context['registerform'] = registerform
            context['registererror'] = registerform.errors
            return render(request, 'user_register.html', context)

