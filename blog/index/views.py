from django.shortcuts import render
from django.core.cache import cache
from read_statistics.utils import get_seven_days_read_date
from read_statistics.utils import get_today_hot_data
from read_statistics.utils import get_yesterday_host_data
from read_statistics.utils import get_7_days_hot_data
from django.contrib.contenttypes.models import ContentType
from blog_index.models import BlogModel

# Create your views here.
# def get_7_days_hot_blogs():
#     today = date.today()
#     dates = today - datetime.timedelta(days=7)
#     blogs = BlogModel.objects.filter(read_date__date__lt=today,
#                                      read_date__date__gte=dates)\
#                                      .values('id', 'title')\
#                                      .annotate(read_num_sum=Sum('read_date__blog_read'))\
#                                      .order_by('-read_num_sum')
#     print(blogs[:3])
#     return blogs[:3]


def index_views(request):
    blog_countent_type = ContentType.objects.get_for_model(BlogModel)
    read_nums, dates = get_seven_days_read_date(blog_countent_type)
    context = {}

    # 获取7天热门博客的缓存数据
    hot_data_for_7_days = cache.get('hot_data_for_7_days')
    if hot_data_for_7_days is None:
        hot_data_for_7_days = get_7_days_hot_data(blog_countent_type)
        cache.set('hot_data_for_7_days', hot_data_for_7_days, 3600)
    print(hot_data_for_7_days)
    context['days'] = dates
    context['read_nums'] = read_nums
    context['today_hot_data'] = get_today_hot_data(blog_countent_type)
    context['yesterday_hot_data'] = get_yesterday_host_data(blog_countent_type)
    context['hot_data_for_7_days'] = hot_data_for_7_days
    return render(request, 'index/index.html', context)
