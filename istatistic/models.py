#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
from iuser.models import Departments
from iservice.models import ServiceInfo
import django.utils.timezone as timezone

# 服务名称、所属部门、服务成本、设备占用（台数）、运行成本（服务续保成本、维修及配件支出、场地信道支出、设备折旧、存储服务成本、节点建设成本）、核算时间、总成本
#按服务统计
class ServiceCost(models.Model):
    name = models.CharField(verbose_name=u'标题', max_length=128,unique=True)
    service_name = models.ForeignKey(ServiceInfo, verbose_name="服务名称")
    department = models.ForeignKey(Departments, verbose_name="所属部门")
    service_cost = models.FloatField(verbose_name=u'服务成本')
    device_used = models.FloatField(verbose_name=u'设备占用(台)')
    renewal_cost = models.FloatField(verbose_name=u'服务续保成本')
    repair_parts_cost =  models.FloatField(verbose_name=u'维修及配件支出')
    channel_cost = models.FloatField(verbose_name=u'场地信道支出')
    device_depreciation = models.FloatField(verbose_name=u'设备折旧')
    storage_cost = models.FloatField(verbose_name=u'存储服务成本')
    node_constructed = models.FloatField(verbose_name=u'节点建设成本')
    total_cost = models.FloatField(verbose_name=u'总成本')
    statistic_time = models.DateTimeField(verbose_name=u'核算时间',default=timezone.now)
    createDate = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True)





# 部门名称、设备占用（台数）、服务成本、运行成本（服务续保成本、维修及配件支出、场地信道支出、设备折旧、存储服务成本、节点建设成本）、核算时间、总成本
#按部门统计
class DepartmentCost(models.Model):
    name = models.CharField(verbose_name=u'标题', max_length=128,unique=True)
    department_name = models.ForeignKey(Departments, verbose_name="部门名称")
    service_cost = models.FloatField(verbose_name=u'服务成本')
    device_used = models.FloatField(verbose_name=u'设备占用(台)')
    renewal_cost = models.FloatField(verbose_name=u'服务续保成本')
    repair_parts_cost =  models.FloatField(verbose_name=u'维修及配件支出')
    channel_cost = models.FloatField(verbose_name=u'场地信道支出')
    device_depreciation = models.FloatField(verbose_name=u'设备折旧')
    storage_cost = models.FloatField(verbose_name=u'存储服务成本')
    node_constructed = models.FloatField(verbose_name=u'节点建设成本')
    total_cost = models.FloatField(verbose_name=u'总成本')
    statistic_time = models.DateTimeField(verbose_name=u'核算时间',default=timezone.now)
    createDate = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True)
