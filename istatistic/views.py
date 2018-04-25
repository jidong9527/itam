#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response
from itam.api import *
# Create your views here.

def service(request):
    return render_to_response('istatistic/statistic_service.html')


def department(request):
    return render_to_response('istatistic/statistic_department.html')

def porject(request):
    return render_to_response('istatistic/statistic_project.html')