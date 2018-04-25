#_*_coding:utf-8_*_
from __future__ import division


import uuid
import urllib
from itam.api import *
from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseNotFound
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@require_role(role='user')
def index(request):
    return render_to_response('index.html')

def Login(request):
    """登录界面"""
    emg = ""
    print request.POST
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    if request.method == 'GET':
        return render_to_response('login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)

                    if user.role == 'su':
                        request.session['role_id'] = 0
                    else:
                        request.session['role_id'] = 1
                    return HttpResponseRedirect(request.session.get('pre_url', '/'))

                else:
                    emg = '用户未激活'
            else:
                emg = '用户名或密码错误'
        else:
            emg = '用户名或密码错误'
    return render_to_response('login.html', {'emg': emg})

@require_role(role='user')
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
@require_role(role='user')
def setting(request):

    return render_to_response('setting.html')
