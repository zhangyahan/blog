from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(BlogReadModel)
class BlogReadAdmin(admin.ModelAdmin):
    # 创建要映射到后台的字段
    list_display = ['blog_read', 'content_object']


@admin.register(ReadDate)
class ReadDateAdmin(admin.ModelAdmin):
    list_display = ['date', 'blog_read', 'content_object']