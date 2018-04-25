#_*_coding:utf-8_*_
from django.db import models


# Create your models here.
# from iasset.models import IDC
from iservice.models import ServiceInfo
from info.models import Contract
from django.conf import settings
from iasset.models import Asset, IDC


STATUS_CHOICES = (
    ('inuse',u'占用'),
    ('unuse',u'未占用'),
)
IP_TYPE_CHOICES = (
    ('ipv4','IPv4'),
    ('ipv6','IPv6'),
)

# PORT_TYPE_CHOICES = (
#     ('twisted-pair',u'双绞线(RJ-45)'),
#     ('multimode-fibre',u'多模光纤'),
#     ('single-fibre',u'单模光纤'),
# )
LINK_TYPE_CHOICES = {
    ('private',u'专线'),
    ('share',u'共享链路'),
}

#IP地址
class IPAddress(models.Model):
    ipaddress = models.GenericIPAddressField(verbose_name=u'IP',unique=True)
    segment = models.ForeignKey('Segment')
    status = models.CharField(verbose_name=u'占用状态',choices=STATUS_CHOICES,max_length=64,default='unuse')
    user = models.CharField(verbose_name=u'占用人',max_length=128,blank=True,null=True)
    service = models.ForeignKey(ServiceInfo, verbose_name=u'服务信息', null=True, blank=True)
    # port = models.ForeignKey(Ports,verbose_name=u'占用端口',null=True,blank=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人',related_name='ip_create_user', null=True,blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人',related_name='ip_update_user', null=True,blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True,null=True)
    class Meta:
        verbose_name = u'IP地址'
        verbose_name_plural = u'IP地址'
#网段
class Segment(models.Model):
    ip_version = models.CharField(verbose_name=u'类型',choices=IP_TYPE_CHOICES,max_length=64,default='ipv4')
    address = models.GenericIPAddressField(verbose_name=u'网段地址')
    mask = models.IntegerField(verbose_name=u'掩码长度')
    usage = models.CharField(verbose_name=u'用途',max_length=256,null=True,blank=True)
    used_num = models.CharField(verbose_name=u'已使用ip数量', max_length=128)
    unused_num = models.CharField(verbose_name=u'未使用ip数量', max_length=128)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='segment_create_user', null=True, blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='segment_update_user', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True,null=True)
    class Meta:
        verbose_name = u'网段'
        verbose_name_plural = u'网段'
        unique_together = ("address", "mask")

# 网络端口

class Ports(models.Model):
    PORT_TYPE_CHOICES = (
        ('twisted-pair', u'双绞线(RJ-45)'),
        ('multimode-fibre', u'多模光纤'),
        ('single-fibre', u'单模光纤'),
        ('virtual', u'虚拟机端口'),
    )
    port_num = models.CharField(verbose_name=u'端口号', max_length=128)
    description = models.CharField(verbose_name=u'端口描述', max_length=256, blank=True, null=True)
    host = models.ForeignKey(Asset, verbose_name=u'占用设备')
    ip = models.ForeignKey('IPAddress', verbose_name=u"IP地址", blank=True, null=True)
    rate = models.CharField(verbose_name=u'端口速率', max_length=64, blank=True, null=True)
    port_type = models.CharField(choices=PORT_TYPE_CHOICES, max_length=64, verbose_name=u"端口类型",
                                 default='twisted-pair', blank=True, null=True)
    connection = models.ForeignKey('self', related_name='connect_to', blank=True, null=True,
                                   verbose_name=u'连接到')
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人',
                                      related_name='ports_create_user', null=True, blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人',
                                      related_name='ports_update_user', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True)

    class Meta:
        verbose_name = u'网络端口'
        verbose_name_plural = u'网络端口'
        unique_together = ("host", "port_num")

#链路

class Link(models.Model):
    # from iasset import models as assetmodels
    name = models.CharField(verbose_name=u'链路名称', max_length=128)
    isp = models.CharField(verbose_name=u'ISP', max_length=128)
    bandwidth = models.CharField(verbose_name=u'带宽', max_length=64)
    link_type = models.CharField(choices=LINK_TYPE_CHOICES,verbose_name=u'链路类型', max_length=64,default='private')
    contract = models.ForeignKey(Contract, verbose_name=u'合同', null=True, blank=True)
    cost = models.FloatField(verbose_name=u'费用',blank=True,null=True)
    start_date = models.DateField(verbose_name=u'起始时间',blank=True,null=True)
    end_date = models.DateField(verbose_name=u'结束时间',blank=True,null=True)
    from_idc = models.ForeignKey(IDC,verbose_name=u'从哪个IDC',related_name='from_idc',null=True,blank=True)
    to_idc = models.ForeignKey(IDC,verbose_name=u'到哪个IDC',related_name='to_idc',null=True,blank=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='link_create_user', null=True, blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='link_update_user', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'链路'
        verbose_name_plural = u'链路'

