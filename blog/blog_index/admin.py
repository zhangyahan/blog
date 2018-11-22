from django.contrib import admin
from .models import *
# Register your models here.


# 创建博客类型的管理类
# 定义要管理那个类
@admin.register(BlogTypeModel)
class BlogTypeAdmin(admin.ModelAdmin):
    # 创建映射到后台的属性（字段）
    list_display = ['blog_type']


# 创建博客的管理类
# 定义要管理那个类
@admin.register(BlogModel)
class BlogAdmin(admin.ModelAdmin):
    # 创建映射到后台的字段
    list_display = ['id','title', 'author','blog_type','blog_read', 'create_time', 'last_update_time']


# @admin.register(BlogReadModel)
# class BlogReadAdmin(admin.ModelAdmin):
#     # 创建要映射到后台的字段
#     list_display = ['blog_read', 'blog']
