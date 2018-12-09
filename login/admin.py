from django.contrib import admin

# Register your models here.

from  . import models

admin.site.register(models.User) #注册到admin后台

admin.site.register(models.ConfirmString) #注册到amdin后台
