#_*_coding:utf-8_*_
__author__ = 'jidong'

from django import forms
from models import ServiceInfo

class ServiceForm(forms.ModelForm):
    class Meta:
        model = ServiceInfo
        # fields = '__all__'
        exclude = ['contract']
        error_messages = {
            'name': {
                'required': u'服务名称需要填写',
                'unique': u'服务名称已存在',
            },
        }