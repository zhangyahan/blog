from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^update_comment/$', update_comment_views, name='update_comment'),
]