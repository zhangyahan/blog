import string
import random
import time
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import send_mail
from .forms import LoginForm, RegisterForm, ChangeNicknameForm, BindEmailForm
from .models import Profile
from blog import settings
# Create your views here.


def login_views(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'index/login.html', context)


def register_views(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username,email,password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))

    else:
        reg_form = RegisterForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'index/register.html', context)


def logout_views(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))


def user_info_views(request):
    context = {}
    return render(request, 'index/user_info.html', context)


def change_nickname_views(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == "POST":
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()

    context = {}
    context['return_back_url'] = redirect_to
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form'] = form
    return render(request, 'form.html', context)


def bind_email_views(request):
    redirect_to = request.GET.get('from', reverse('index'))
    if request.method == "POST":
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()

    context = {}
    context['return_back_url'] = redirect_to
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    return render(request, 'index/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', '')
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session['bind_email_code'] = code
            request.session['send_code_time'] = now

        # 发送邮件
        send_mail(
            '绑定邮箱',
            '验证码: {}'.format(code),
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
