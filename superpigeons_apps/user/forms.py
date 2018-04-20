from django import forms
from django.core.exceptions import ValidationError
# from superpigeons_apps.user.models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import re


class LoginForm(forms.Form):
    # 用户登录表单
    def clean_username(self):
        # 验证用户名是否存在
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise ValidationError('用户不存在')
        return username

    def clean_password(self):
        # 验证密码
        password = self.cleaned_data.get("password")
        username = self.cleaned_data.get("username")
        loginuser = authenticate(username=username, password=password)
        if not User.objects.filter(username=username).exists():
            return password
        else:
            if loginuser is None:
                raise ValidationError("密码错误")
            return password

    username = forms.CharField(
        required=True,
        min_length=6,
        label=u'Username',
        error_messages={'required': u'请输入用户名'},
        widget=forms.TextInput(attrs={'placeholder': u'用户名', 'class': u'form-control'}),
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        label=u'Password',
        error_messages={'required': u'请输入密码', 'min_length': u'至少输入6位密码'},
        widget=forms.PasswordInput(attrs={'placeholder': u'密 码', 'class': u'form-control'}),
    )


class RegisterForm(forms.Form):
    # 用户注册表单
    def clean_useremail(self):
        useremail = self.cleaned_data.get("useremail")
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',useremail):
            raise ValidationError('电子邮箱格式错误')
        return useremail

    def clean_passwordagain(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("passwordagain")
        if password1 != password2:
            raise ValidationError('再次确认密码错误')
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError('用户已经存在')
        return username

    username = forms.CharField(
        required=True,
        label=u'用户名',
        widget=forms.TextInput(attrs={'placeholder': u'用户名', 'class': u'text'}),
    )
    password = forms.CharField(
        required=True,
        min_length=8,
        label=u'密 码',
        error_messages={'required': u'请输入密码', 'min_length': u'至少输入6位密码'},
        widget=forms.PasswordInput(attrs={'placeholder': u'密 码', 'class': u'text'}),
    )
    passwordagain = forms.CharField(
        # validators=[repassword],
        required=True,
        min_length=6,
        label=u'确认密码',
        error_messages={'required': u'请输入密码', 'min_length': u'至少输入6位密码'},
        widget=forms.PasswordInput(attrs={'placeholder': u'确认密码', 'class': u'text'}),
    )
    # nikename = forms.CharField(
    #     required=True,
    #     min_length=4,
    #     label=u'昵称',
    #     error_messages={'required': u'请输入昵称','min_length':u'至少输入4位昵称'},
    #     widget=forms.TextInput(attrs={'placeholder': u'昵称', 'class': u'text'}),
    # )
    useremail = forms.CharField(
        # validators=[email_validate],
        required=True,
        label=u'邮箱',
        widget=forms.EmailInput(attrs={'placeholder': u'邮箱', 'class': u'text'}),
    )


class ModifyForm(forms.Form):
    # 用户补充资料表单
    headpic=forms.ImageField(
    )
    phone = forms.IntegerField(
        label=u'手机',
        widget=forms.TextInput(attrs={'placeholder': u'手机', 'class': u'modify'}),
    )
    address = forms.CharField(
        label=u'地址',
        widget=forms.TextInput(attrs={'placeholder': u'地址', 'class': u'modify'}),
    )
    interst = forms.CharField(
        label=u'兴趣',
        widget=forms.TextInput(attrs={'placeholder': u'兴趣', 'class': u'modify'}),
    )
