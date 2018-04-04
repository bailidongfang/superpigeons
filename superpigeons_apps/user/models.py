from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tags(models.Model):
    tagname=models.CharField(max_length=20)

class UserInfo(models.Model):
    user=models.OneToOneField(User,primary_key=True)
    username=models.CharField(max_length=20)
    nickname=models.CharField(max_length=20,default='')
    sign=models.CharField(max_length=500,default='这个人很懒，什么都没有留下')
    score=models.IntegerField(default=0)
    level=models.CharField(max_length=20,default='实习小编')
    tags=models.ManyToManyField(Tags)
    headpic=models.ImageField(upload_to='headpic')

class UserScore(models.Model):
    username=models.CharField(max_length=20)
    type=models.CharField(max_length=5)
    score=models.IntegerField()
    time=models.DateTimeField(auto_now_add=True)

