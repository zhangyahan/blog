from django.conf.urls import url
from .views import *

urlpatterns = [
    # 处理 blog/的路径， 返回博客列表
    url(r'^$', blog_list_views, name='blog_list'),
    # 处理 blog/博客id 的路径,返回博客具体内容
    url(r'^blog_content/(\d*)/$', blog_content_views, name='blog_content'),
    # 处理博客分类列表的路径根据分类的id返回对应分类的博客
    url(r'^blog_type/(\w+)/$', blog_type_list_views, name='type_list'),
    # 根据博客发布时间进行相对应的返回
    url(r'^blog_date/(\d{4})/(\d{1,2})/(\d{1,2})/$', blog_date_views, name='blog_date'),
]