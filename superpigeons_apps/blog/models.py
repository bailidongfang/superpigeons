from django.db import models
from django.contrib.auth.models import User
from superpigeons_apps.user.models import UserInfo
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    auther = models.ForeignKey(User)
    title = models.TextField(max_length=50)
    text = RichTextUploadingField()
    add_date = models.DateTimeField(auto_now_add=True)
    mod_date = models.DateTimeField(auto_now=True)


class ArticleSeen(models.Model):
    id = models.AutoField(primary_key=True)
    seener = models.ForeignKey(User)
    seen_article = models.ForeignKey(Article)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_article = models.ForeignKey(Article)
    commenter = models.ForeignKey(User)
    text = models.TextField(default='')
    date = models.DateTimeField(auto_now_add=True)


class CommentUp(models.Model):
    id = models.AutoField(primary_key=True)
    comment_uper = models.ForeignKey(User)
    comment_article = models.ForeignKey(Comment)


