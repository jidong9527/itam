#_*_coding:utf-8_*_
__author__ = 'jidong'

from settings import *
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from datetime import datetime,date
import json
from IPy import IP

def http_success(request, msg):
    return render_to_response('success.html', locals())

def http_error(request, emg):
    message = emg
    return render_to_response('error.html', locals())

def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))

class ServerError(Exception):
    """
    self define exception
    自定义异常
    """
    pass

def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    paginator = Paginator(post_objects, int(request.GET.get('pageSize', '10')))    #指定每页显示行数
    try:
        current_page = int(request.GET.get('pageNumber', '1'))
    except ValueError:
        current_page = 1
    # print paginator,current_page
    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end


# def pages(post_objects, request):
#     """
#     page public function , return page's object tuple
#     分页公用函数，返回分页的对象元组
#     """
#     paginator = Paginator(post_objects, 20)    #指定每页显示20条数据
#     try:
#         current_page = int(request.GET.get('page', '1'))
#     except ValueError:
#         current_page = 1
#
#     page_range = page_list_return(len(paginator.page_range), current_page)
#
#     try:
#         page_objects = paginator.page(current_page)
#     except (EmptyPage, InvalidPage):
#         page_objects = paginator.page(paginator.num_pages)
#
#     if current_page >= 5:
#         show_first = 1
#     else:
#         show_first = 0
#
#     if current_page <= (len(paginator.page_range) - 3):
#         show_end = 1
#     else:
#         show_end = 0
#
#     # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
#     return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end


def class_to_dict(obj):
    '''把models对象转换成字典格式'''
    obj_attr_list = obj._meta.get_all_field_names()   #获取数据库表中的字段名
    obj_attr_dict = {}
    obj_dict = obj.__dict__
    # print 'obj_attr_list:',obj_attr_list
    # print 'obj_dict:',obj_dict
    for attr in obj_attr_list:
        # dict[attr] = obj.__getattribute__(attr):
        if obj_dict.has_key(attr):
            obj_attr_dict[attr] = obj_dict[attr]
        else:
            obj_attr_dict[attr] = ''
    return obj_attr_dict

class DatetimeEncoder(json.JSONEncoder):
    """
    python datetime不支持json序列化的 解决办法
    """
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)

def require_role(role='user'):
    """
    decorator for require user role in ["super", "admin", "user"]
    要求用户是某种角色 ["super", "admin", "user"]的装饰器
    """

    def _deco(func):
        def __deco(request, *args, **kwargs):
            request.session['pre_url'] = request.path
            if not request.user.is_authenticated():
                return HttpResponseRedirect(reverse('login'))
            if role == 'admin':
                # if request.session.get('role_id', 0) < 1:
                if request.user.role == 'cu':
                    return HttpResponseRedirect(reverse('index'))
            elif role == 'super':
                # if request.session.get('role_id', 0) < 2:
                if request.user.role == 'cu':
                    return HttpResponseRedirect(reverse('index'))
            return func(request, *args, **kwargs)

        return __deco

    return _deco

#根据choices中的元组的value，取出元组的key
def choice_code(key, value):
    """
    key表示choices元组的名称，先将元组转换成字典，找出value对应的key
    """
    for k,v in dict(key).iteritems():
        if v.encode("utf-8") == value:
            return k
#验证IP地址格式的正确性
def valid_ip(address):
    try:
        IP(address)
    except:
        return False
    else:
        return True
