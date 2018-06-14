from django.db import models
from django.contrib.auth.models import User
from superpigeons_apps.user.models import UserInfo
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.


class Tags(models.Model):
    id = models.AutoField(primary_key=True)
    is_common = models.BooleanField()
    commenter = models.ForeignKey(User)
    tag_name = models.TextField(max_length=30,default='')


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    auther = models.ForeignKey(User)
    title = models.TextField(max_length=50)
    text = RichTextUploadingField()
    tags = models.ManyToManyField(Tags)
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)
    comment_count = models.IntegerField(default=0)
    seen_count = models.IntegerField(default=0)


class ArticleSeen(models.Model):
    id = models.AutoField(primary_key=True)
    seen_csrf = models.TextField(max_length=50, default='1')
    seener = models.TextField(max_length=50, default='')
    seen_article = models.ForeignKey(Article)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_article = models.ForeignKey(Article, null=True, default='')
    recomment_tree = models.ForeignKey('self', related_name='tree', null=True, default='')
    recomment_target = models.ForeignKey('self', null=True, default='')
    commenter = models.ForeignKey(User)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)


class CommentUp(models.Model):
    id = models.AutoField(primary_key=True)
    comment_uper = models.ForeignKey(User)
    comment_article = models.ForeignKey(Comment)


