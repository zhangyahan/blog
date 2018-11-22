"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [


    url(r'^admin/', admin.site.urls),
    # 将blog的网址交给blog_index文件中urls去处理
    url(r'^blog/', include('blog_index.urls')),
    # 配置富文本url,用于接收内容
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    # 配置评论路由
    url(r'^comment/', include('comment.urls')),

    url(r'^user/', include('user.urls')),
    # 首页
    url(r'^', include('index.urls')),

]
# 配置上传地址
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)