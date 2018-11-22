from django.db import models
# 引用后台管理员
from django.contrib.auth.models import User
# ckeditor_uploader.fields中的RichTextUploadingField是用来定义富文本的,用于上传文本和图片
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import test, ReadDate
from django.contrib.contenttypes.fields import GenericRelation


# 先修改数据库为mysql
# 创建博客分类表
class BlogTypeModel(models.Model):
    # 创建博客分类字段
    blog_type = models.CharField(max_length=32, verbose_name='博客类型')

    # 返回的数据格式
    def __str__(self):
        return '{}'.format(self.blog_type)

    # 定义内部类， 在数据库中的表名，和后台的表名
    class Meta:
        db_table = 'blog_type'
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name


# 创建博客表,继承test类,当中有一个blog_read方法
class BlogModel(models.Model, test):
    # 博客标题
    title = models.CharField(max_length=50, verbose_name='博客标题')
    # 博客分类，引用博客分类表，多个博客有一个分类
    blog_type = models.ForeignKey(BlogTypeModel, verbose_name='博客分类')
    # 博客内容,当前为富文本,
    content = RichTextUploadingField(verbose_name='博客内容')
    # 博客作者，引用后台管理员的user
    author = models.ForeignKey(User, verbose_name='作者')
    # 阅读数
    read_date = GenericRelation(ReadDate)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    # 最后修改时间
    last_update_time = models.DateTimeField(auto_now=True, verbose_name='最后修改时间')

    # 返回的数据格式
    def __str__(self):
        return '{}'.format(self.title)

    # 定义内部类， 在数据库中的表名，和后台的表名
    class Meta:
        db_table = 'blog'
        verbose_name = '博客'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']


