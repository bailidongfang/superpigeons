from django.contrib import admin
from superpigeons_apps.blog.models import Article,Comment
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)

