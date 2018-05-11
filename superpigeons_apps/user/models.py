from django.db import models
from django.contrib.auth.models import User
from storages.backends.ftp import FTPStorage
# from storages.backends.sftpstorage import SFTPStorage
# Create your models here.
headpic_path='headpic'


class Interest(models.Model):
    interestname = models.CharField(max_length=20)


class UserInfo(models.Model):
    fs = FTPStorage()
    user = models.OneToOneField(User, primary_key=True)
    username = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    sign = models.CharField(max_length=500, default='这个人很懒，什么都没有留下')
    score = models.IntegerField(default=0)
    level = models.CharField(max_length=20, default='实习小编')
    interest = models.ManyToManyField(Interest, null=True)
    headpic = models.ImageField(upload_to=headpic_path, storage=fs, null=True)


class UserScore(models.Model):
    username = models.CharField(max_length=20)
    type = models.CharField(max_length=5)
    score = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

