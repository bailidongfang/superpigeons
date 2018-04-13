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
    comment_count = models.IntegerField(default=0)
    seen_count = models.IntegerField(default=0)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article)
    id = models.AutoField(primary_key=True)
    commenter = models.CharField(max_length=20)
    userinfo=models.ForeignKey(UserInfo)
    comment_text = models.CharField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_up_count = models.IntegerField(default=0)


class CommentUp(models.Model):
    comment_uper = models.CharField(max_length=100)
    comment = models.ForeignKey(ArticleComment)
    is_comment = models.NullBooleanField()


