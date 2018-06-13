from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from superpigeons_apps.user.forms import LoginForm, RegisterForm
from superpigeons_apps.user.models import UserInfo, headpic_path
from superpigeons_apps.blog.models import Article
from superpigeons_apps.blog.views import blog_edit
from django.db import transaction
from common.FromFtp import headpic_to_ftp
from common.ImagePillow import crop_image
from common.Decorator import user_inter_permission
from common.level import Level
import traceback
# Create your views here.


# 我的信息
@user_inter_permission
def user_my_info(request, username):
    userinfo = UserInfo.objects.get(username=username)
    context = dict()
    context['userinfo'] = userinfo
    context['user'] = request.user
    return render(request, 'user_info.html', context)


# 我的信息-修改信息
@user_inter_permission
def user_my_info_userinfo(request):
    try:
        username = request.POST['permission_name']
        nickname = request.POST['nickname']
        sign = request.POST['sign']
        userinfo = UserInfo.objects.get(username=username)
        userinfo.nickname = nickname
        userinfo.sign = sign
        userinfo.save()
    except Exception as e:
        traceback.print_exc()
        return HttpResponse(e)
    else:
        return HttpResponse('success')
# 我的信息-修改头像
@user_inter_permission
def user_my_info_headpic(request):
    # 剪裁数据获取
    username = request.POST['permission_name']
    headpic_name = headpic_path+'/'+str(username)+'.jpg'
    file = request.FILES['avatar_file']
    top = int(float(request.POST['avatar_y']))
    buttom = top + int(float(request.POST['avatar_height']))
    left = int(float(request.POST['avatar_x']))
    right = left + int(float(request.POST['avatar_width']))
    # 剪裁头像
    crop_file = crop_image(file, left, top, right, buttom)
    # 上传头像
    headpic_to_ftp(headpic_name, crop_file)
    # 修改头像信息
    userinfo = UserInfo.objects.get(username=username)
    userinfo.headpic = headpic_name
    userinfo.save()
    return HttpResponse("success")


# 我的主页
def user_index(request, username):
    userinfo = UserInfo.objects.get(username=username)
    articles = Article.objects.filter(auther__username=username)
    context = dict()
    if str(request.user) == username:
        context['permission'] = 'ture'
    else:
        context['permission'] = 'false'
    context['userinfo'] = userinfo
    context['articles'] = articles
    return render(request, 'user_index.html', context)


# 我的主页-删除博客
def user_index_inter(request):
    if request.POST['type'] == 'delete':
        rst = blog_edit(request, **{'ftype': 'delete', 'artid': request.POST['article_id']})
        return HttpResponse(rst)


# 登陆
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
            lev = Level(formusername)
            lev.comput_level("a")
            return redirect('index')
        else:
            context['loginform'] = loginform
            return render(request, 'user_login.html', context)


# 注销
def user_logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return redirect('index')


# 注册
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

