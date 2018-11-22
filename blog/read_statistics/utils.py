from datetime import date
import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import BlogReadModel, ReadDate


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)  # 根据模型名称,获取当前模型
    key = '{}_{}_read'.format(ct.model, obj.id)  # 创建cookies, ct.model获取模型名, obj.id获取模型中的id值
    if not request.COOKIES.get(key):  # 如果获取不到cookies
        blogread, created = BlogReadModel.objects.get_or_create(content_type=ct, object_id=obj.id)  # 创建并获取博客总阅读量
        blogread.blog_read += 1  # 阅读量+1
        blogread.save()  # 保存
        readDate, created = ReadDate.objects.get_or_create(content_type=ct, object_id=obj.id, date=date.today())  # 获取或创建当天阅读数并+1
        readDate.blog_read += 1
        readDate.save()
    return key  # 返回cookie


# 分别获取七日阅读量
def get_seven_days_read_date(content_type):
    today = date.today()
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        day = today - datetime.timedelta(days=i)
        dates.append(day.strftime('%m/%d'))
        read_day = ReadDate.objects.filter(content_type=content_type, date=day)
        result = read_day.aggregate(blog_read_sum=Sum('blog_read'))  # 求和
        read_nums.append(result['blog_read_sum'] or 0)

    return read_nums, dates


def get_today_hot_data(content_type):
    today = date.today()
    read_datails = ReadDate.objects.filter(content_type=content_type, date=today).order_by('-blog_read')
    return read_datails[:3]


def get_yesterday_host_data(content_type):
    today = date.today()
    yesterday = today - datetime.timedelta(days=1)
    read_datails = ReadDate.objects.filter(content_type=content_type, date=yesterday).order_by('-blog_read')
    return read_datails[:3]


def get_7_days_hot_data(content_type):
    today = date.today()
    dates = today - datetime.timedelta(days=7)

    read_datails = ReadDate.objects.filter(content_type=content_type,
                                           date__lt=today,
                                           date__gte=dates,)\
                                           .values('content_type', 'object_id')\
                                           .annotate(read_num_sum=Sum('blog_read'))\
                                           .order_by('-read_num_sum').all()
    return read_datails[:3]