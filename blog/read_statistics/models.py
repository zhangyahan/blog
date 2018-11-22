from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from datetime import date


# Create your models here.
class BlogReadModel(models.Model):
    # 创建阅读表,该字段为阅读数量
    blog_read = models.IntegerField(default=0, verbose_name='阅读量')
    # 外键直接引用ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    # 记录对应模型的主键值
    object_id = models.PositiveIntegerField()
    #
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        db_table = 'blog_read'
        verbose_name = '阅读量'
        verbose_name_plural = verbose_name


class test(object):
    def blog_read(self):
        # 使用模型的类名获取当前模型
        ct = ContentType.objects.get_for_model(self)
        try:
            # 使用当前对象的id和当前模型获取当前阅读数量
            readnum = BlogReadModel.objects.get(content_type=ct, object_id=self.id)
            return readnum.blog_read
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDate(models.Model):
    date = models.DateField(default=date.today)
    blog_read = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
