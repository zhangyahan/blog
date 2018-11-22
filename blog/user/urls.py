from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^login/$', login_views, name='login'),
    url(r'^register/$', register_views, name='register'),
    url(r'^logout/$', logout_views, name='logout'),
    url(r'^user_info/$', user_info_views, name='user_info'),
    url(r'^change_nickname/$', change_nickname_views, name='change_nickname'),
    url(r'^bind_email/$', bind_email_views, name='bind_email'),
    url(r'^bind_email_send_code/$', send_verification_code, name='send_code')
]
