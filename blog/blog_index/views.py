from django.shortcuts import render, HttpResponse
from django.contrib.contenttypes.models import ContentType
# 导入当前文件的数据库模型
from .models import *
# Create your views here.
from django.core.paginator import Paginator
from django.conf import settings
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm


# 博客分页功能
def get_base_blog(request, blog_list_all):
    # 获取全部博客列表并进行分页
    paginator = Paginator(blog_list_all, settings.EACH_PAGE_BLOG_NUMBER)  # # 每2篇进行分页
    # 获取get请求的页数, 如果获取不到返回第一页
    page_num = request.GET.get('page', 1)  # 获取页码参数(GET请求)
    try:
        # 获取用户点击的页数
        page_od_blog = paginator.page(page_num)
    except:
        # 如果没有返回第一页
        page_od_blog = paginator.page(1)

    currentr_page_num = page_od_blog.number  # 获取当前页
    # 控制当前页的左右两页, 进行逻辑判断, 前两页不能比1小,后两页不能比当前总页数大, num_pages获取总页数
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))

    # 添加省略号标记,首页省略号, 当第一个页码-1大于等于2时, 就需要加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    # 当当前页减去最后一页大于等于2时, 尾部也需要加上省略号
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 判断首页和尾页是否在页码中,如果不在则添加上
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_list = page_od_blog  # 用户当前点击页数
    blog_type = BlogTypeModel.objects.all()  # 博客类型列表
    blog_date = BlogModel.objects.dates('create_time', 'day', order='DESC')  # 博客发布时间, 年月日, 时间倒序
    return locals()  # 返回用户当前点击页, 博客类型, 发布时间, 页码列表


# 博客列表视图
def blog_list_views(request):
    blog_list_all = BlogModel.objects.all()  # 查询所有的博客
    base_dic = get_base_blog(request, blog_list_all)
    blog_type = BlogTypeModel.objects.all()
    return render(request, 'blog/blog_list.html', locals())


# 博客分类，根据不同的分类id返回不同的分类博客
def blog_type_list_views(request, type_id):
    blog_list_all = BlogModel.objects.filter(blog_type=type_id).all()  # 查询所有的博客
    base_dic = get_base_blog(request, blog_list_all)
    type_name = BlogTypeModel.objects.get(id=type_id)
    return render(request, 'blog/blog_type.html', locals())


# 时间归档, 根据年月日, 返回年月日的博客
def blog_date_views(request, year, month, day):
    blog_list_all = BlogModel.objects.filter(create_time__year=year,
                                             create_time__month=month,
                                             create_time__day=day)  # 查询所有的博客
    base_dic = get_base_blog(request, blog_list_all)
    blogs_date = '%s年%s月%s日' % (year, month, day)
    return render(request, 'blog/blog_date.html', locals())


# 具体的博客内容, 接受博客id进行返回具体的博客内容
def blog_content_views(request, blog_id):
    blog = BlogModel.objects.get(id=blog_id)  # 获取用户点击的博客id
    read_cookie_key = read_statistics_once_read(request, blog)  # read_statistics_once_read返回当前博客的cookie

    last_blog = BlogModel.objects.filter(create_time__gt=blog.create_time).last()
    next_blog = BlogModel.objects.filter(create_time__lt=blog.create_time).first()

    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,
                                      object_id=blog.id,
                                      parent=None).order_by('-comment_time')
    comment_count = Comment.objects.filter(content_type=blog_content_type,
                                           object_id=blog.id).count()

    data = {
        'content_type': blog_content_type.model,
        'object_id': blog.id,
        'reply_comment_id': '0',
    }
    comment_form = CommentForm(initial=data)

    # 构建响应对象
    response = render(request, 'blog/blog_content.html', locals())
    response.set_cookie(read_cookie_key, 'true', max_age=60*60*24)
    if blog:
        return response
    else:
        return HttpResponse("对不起,该博客以消失")
