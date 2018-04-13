from django.contrib import admin
from superpigeons_apps.user.models import UserInfo,Interest
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Interest)