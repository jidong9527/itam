#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response
from itam.api import *
# Create your views here.

def log_list(request):
    return render_to_response('ilog/log_list.html')