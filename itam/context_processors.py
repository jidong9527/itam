#_*_coding:utf-8_*_
__author__ = 'jidong'

from iuser.models import User
from iasset.models import Asset
from itam.api import *
from iservice.models import ServiceInfo


def name_proc(request):
    user_id = request.user.id
    role_id = {'su': 0, 'cu': 1}.get(request.user.role, 0)
    # role_id = 'SU'
    user_total_num = User.objects.all().count()
    user_active_num = User.objects.filter(is_active=True).count()
    asset_total_num = Asset.objects.all().count()
    service_online_num = ServiceInfo.objects.filter(status='online').count() #上线服务数量
    service_total_num = ServiceInfo.objects.all().count()  #所有服务数量
    # host_active_num = Asset.objects.filter(is_active=True).count()
    request.session.set_expiry(3600)

    info_dic = {'session_user_id': user_id,
                'session_role_id': role_id,
                'user_total_num': user_total_num,
                'user_active_num': user_active_num,
                'asset_total_num': asset_total_num,
                'service_online_num': service_online_num,
                'service_total_num': service_total_num,
                }

    return info_dic

