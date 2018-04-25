#_*_coding:utf-8_*_
from django.db import models
# from iuser.models import User
from iservice.models import ServiceInfo
from info.models import Contract, Contacts, Company, ProductModel
# from inetwork.models import IPAddress
from django.conf import settings
# Create your models here.
from share import ASSET_TYPE_CHOICES

DEVICE_STATUS = (
    ('purchasing',u'采购'),
    ('unuse',u'未用'),
    ('inuse',u'在用'),
    ('loan',u'借出'),
    ('troubling',u'故障'),
    ('maintaining',u'维修'),
    ('off',u'下架'),
    ('abandoned',u'报废'),
)
SIMPLE_STATUS_CHOICES = (
    ('available',u'可用'),
    ('unavailable',u'不可用'),
)

OS_TYPE_CHOICES = (
    ('linux','Linux'),
    ('unix','unix'),
    ('windows','Windows'),
)

SELF_OR_LEASE_CHOICES = (
    ('self',u'自有'),
    ('lease',u'租借'),
)

#资产表
class Asset(models.Model):
    asset_number = models.CharField(verbose_name=u'资产编号',max_length=128,null=True,blank=True)  #租借的设备可能没有资产编号
    name = models.CharField(verbose_name=u'设备名称',max_length=128,unique=True)
    sn = models.CharField(verbose_name=u'序列号', max_length=128, null=True, blank=True)
    model = models.ForeignKey(ProductModel, verbose_name=u'设备型号', related_name='relatedmodel', null=True, blank=True)
    # isself = models.CharField(verbose_name=u'购买/租借',choices=SELF_OR_LEASE_CHOICES,max_length=16, default='self')
    contract = models.ManyToManyField(Contract, verbose_name=u'合同')
    purchase_date = models.DateField(verbose_name=u'购买时间',null=True, blank=True)
    warranty_period = models.SmallIntegerField(verbose_name=u"质保年限",null=True, blank=True)
    expire_date = models.DateField(verbose_name=u'过保时间',null=True, blank=True)
    cost = models.FloatField(verbose_name=u'成本',null=True, blank=True)
    renewal_date = models.DateField(verbose_name=u'续保时间',null=True, blank=True)
    renewal_cost = models.FloatField(verbose_name=u'续保成本',null=True, blank=True)
    total_cost = models.FloatField(verbose_name=u'资产总值',null=True,blank=True)  #根据配件的添加，续保，折旧，自动计算得出
    asset_admin = models.CharField(verbose_name=u'设备管理员',max_length=64,null=True, blank=True)
    status = models.CharField(verbose_name=u'设备状态',choices=DEVICE_STATUS,default='unuse',max_length=128)
    online_date = models.DateField(verbose_name=u'上架时间', null=True, blank=True)
    offline_date = models.DateField(verbose_name=u'下架时间', null=True, blank=True)
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'创建人',null=True, blank=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='asset_create_user', null=True, blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='asset_update_user', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',blank=True, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'最后更新时间',blank=True, auto_now=True)
    # tags = models.ManyToManyField('Tag', verbose_name=u'标签',blank=True)
    qrcode = models.ImageField(verbose_name=u'二维码',upload_to='iasset/qrcode/',null=True,blank=True)
    picture = models.ImageField(verbose_name=u'设备图片',upload_to='iasset/img/',null=True,blank=True)
    parts = models.ManyToManyField('Parts', related_name='asset_parts', verbose_name=u'配件')
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'资产总表'
        verbose_name_plural = u"资产总表"
    def __unicode__(self):
        return self.asset_number

#设备基类
class DeviceBase(models.Model):
    asset = models.OneToOneField('Asset')
    cabinet = models.ForeignKey('Cabinet', verbose_name=u'所在机柜', null=True, blank=True)
    location = models.SmallIntegerField(verbose_name=u'设备位置', null=True, blank=True)
    os_release = models.ForeignKey('OS', verbose_name=u'操作系统版本', blank=True, null=True)
    service = models.ForeignKey(ServiceInfo, verbose_name=u'服务信息', blank=True,null=True)
    raid_type = models.CharField(verbose_name=u'raid类型', max_length=512, blank=True, null=True)
    storage_used = models.ForeignKey('StorageSpace', verbose_name=u'存储空间使用', blank=True, null=True)
    cpu_count = models.SmallIntegerField(verbose_name=u'CPU核数',blank=True,null=True)
    cpu_model = models.CharField(verbose_name=u'CPU型号',max_length=128,blank=True,null=True)
    memory = models.FloatField(verbose_name=u'内存大小(G)',blank=True,null=True)
    disk = models.FloatField(verbose_name=u'磁盘容量(G)',blank=True,null=True)
    # memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        abstract = True
    def __unicode__(self):
        return self.asset.name

#架式/塔式服务器
class Server(DeviceBase):
    class Meta:
        verbose_name = u'服务器'
        verbose_name_plural = u"服务器"
#刀箱
class BladeCenter(DeviceBase):
    slotSum = models.SmallIntegerField(verbose_name=u'槽位总数',null=True,blank=True)
    class Meta:
        verbose_name = u'刀箱'
        verbose_name_plural = u'刀箱'

#刀片服务器
class Blade(DeviceBase):
    bladecenter = models.ForeignKey('BladeCenter',verbose_name=u'所属刀箱',null=True,blank=True)
    slotNum = models.SmallIntegerField(verbose_name=u'槽位',null=True,blank=True)
    class Meta:
        verbose_name = u'刀片服务器'
        verbose_name_plural = u"刀片服务器"
        #together = ["sn", "asset"]

#虚拟机
# class VM(models.Model):
class VM(DeviceBase):
    # asset = models.OneToOneField('Asset')
    host = models.ForeignKey('Asset', related_name='vm_host', verbose_name=u"宿主机")
    # cpu = models.SmallIntegerField(verbose_name=u'CPU个数', blank=True, null=True)
    # memory = models.FloatField(verbose_name=u'内存大小(G)', blank=True, null=True)
    # disk = models.FloatField(verbose_name=u'硬盘大小(G)', blank=True, null=True)
    # os_release = models.ForeignKey('OS', verbose_name=u'操作系统版本', blank=True, null=True)
    # storage_used = models.ForeignKey('StorageSpace', verbose_name=u'存储空间使用', blank=True, null=True)
    # raid_type = models.CharField(verbose_name=u'raid类型', max_length=128, blank=True, null=True)
    class Meta:
        verbose_name = u'虚拟机'
        verbose_name_plural = u'虚拟机'

#网络设备
class Network(DeviceBase):
    class Meta:
        verbose_name = u'网络设备'
        verbose_name_plural = u'网络设备'

#存储设备
class Storage(DeviceBase):
    total_storage = models.FloatField(verbose_name=u'存储总量(G)', blank=True, null=True)
    class Meta:
        verbose_name = u'存储设备'
        verbose_name_plural = u'存储设备'

#带库
class Tape(DeviceBase):
    total = models.IntegerField(verbose_name=u'磁带总量(盘)', blank=True, null=True)
    used = models.IntegerField(verbose_name=u'已用(盘)', blank=True, null=True)
    # size = models.IntegerField(verbose_name=u'单盘磁带容量(G)', blank=True, null=True)
    specification = models.CharField(verbose_name=u'磁带规格', max_length=128, blank=True, null=True)
    class Meta:
        verbose_name = u'磁带库'
        verbose_name_plural = u'磁带库'

#存储空间
class StorageSpace(models.Model):
    name = models.CharField(verbose_name=u'名称', max_length=128, unique=True)
    host_on = models.ForeignKey('Storage', verbose_name=u'存储主机')
    volume = models.IntegerField(verbose_name=u'空间容量(G)')
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='storagespace_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='storagespace_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',blank=True, auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'最后更新时间',blank=True, auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'存储空间'
        verbose_name_plural = u'存储空间'

#安全设备
class Security(DeviceBase):
    class Meta:
        verbose_name = u'安全设备'
        verbose_name_plural = u'安全设备'

# 其他设备
class Others(DeviceBase):
    class Meta:
        verbose_name = u'其它设备'
        verbose_name_plural = u'其它设备'

# CPU配件
# class CPU(models.Model):
#     asset = models.OneToOneField('Asset')
#     # cpuModel = models.CharField(u'CPU型号', max_length=128,blank=True)
#     # cpuCount = models.SmallIntegerField(u'物理cpu个数')
#     cpuCoreCount = models.SmallIntegerField(u'核数',blank=True,null=True)
#     frequency = models.FloatField(u'主频',blank=True,null=True)
#     user = models.ForeignKey('Asset',related_name='cpu_user',verbose_name=u'使用者',blank=True,null=True)
#     class Meta:
#         verbose_name = u'CPU配件'
#         verbose_name_plural = u"CPU配件"
#
#     def __unicode__(self):
#         return self.cpuModel

# 内存条配件
# class RAM(models.Model):
#     asset = models.ForeignKey('Asset')
#     capacity = models.IntegerField(u'内存大小(G)',blank=True,null=True)
#     user = models.ForeignKey('Asset', related_name='ram_user', verbose_name=u'使用者',blank=True, null=True)
#     def __unicode__(self):
#         return self.asset.name
#     class Meta:
#         verbose_name = u'内存条'
#         verbose_name_plural = u"内存条"

# 硬盘
# class Disk(models.Model):
#     asset = models.ForeignKey('Asset')
#     capacity = models.FloatField(u'磁盘容量GB',blank=True,null=True)
#     iface_type = models.CharField(u'接口类型', max_length=64, blank=True, null=True)
#     user = models.ForeignKey('Asset', related_name='disk_user', verbose_name=u'使用者',blank=True, null=True)
#     class Meta:
#         verbose_name = u'硬盘'
#         verbose_name_plural = u"硬盘"
#
#     def __unicode__(self):
#         return self.asset.name

# 网卡组件
# class NIC(models.Model):
#     asset = models.ForeignKey('Asset')
#     macaddress = models.CharField(u'MAC', max_length=64, unique=True)
#     speed = models.IntegerField(u"传输速度(Mbps)",blank=True,null=True)
#     user = models.ForeignKey('Asset', related_name='nic_user', verbose_name=u'使用者',blank=True, null=True)
#     def __unicode__(self):
#         return self.asset.name
#     class Meta:
#         verbose_name = u'网卡'
#         verbose_name_plural = u"网卡"

# class CabinetType(models.Model):
#     name = models.CharField(verbose_name=u'机柜类型名称',max_length=256,unique=True)
#     status = models.CharField(choices=SIMPLE_STATUS_CHOICES, verbose_name=u'状态',max_length=16, default='available')
#     create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
#     update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
#     memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
#     class Meta:
#         verbose_name = u'机柜类型'
#         verbose_name_plural = u'机柜类型'

# 机柜
class Cabinet(models.Model):
    # asset = models.OneToOneField('Asset')
    name = models.CharField(verbose_name=u'机柜名称',max_length=256,unique=True)
    # cabinet_type = models.ForeignKey('CabinetType')
    idc = models.ForeignKey('IDC', verbose_name=u'所在机房',null=True, blank=True)
    location = models.CharField(verbose_name=u'位置',max_length=256,null=True, blank=True)
    layer = models.IntegerField(verbose_name=u'总层数',default=42)
    specifications = models.CharField(verbose_name=u'规格',max_length=128,blank=True,null=True) #长宽高等
    status = models.CharField(choices=SIMPLE_STATUS_CHOICES, verbose_name=u'状态',max_length=16, default='available')
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='cabinet_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='cabinet_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'机柜'
        verbose_name_plural = u'机柜'

# 机房设备(摄像头)
# class IDCDevice(models.Model):
#     asset = models.OneToOneField('Asset')
#     class Meta:
#         verbose_name = u'机房配套设备'
#         verbose_name_plural = u'机房配套设备'

# 配件（硬盘，内存条，网卡，摄像头等）
class Parts(models.Model):
    PARTS_CHOICES = (
        ('nic', u'网卡'),
        ('cpu', u'处理器'),
        ('memory', u'内存条'),
        ('disk', u'硬盘'),
        ('camera', u'摄像头'),
        ('others', u'其他'),
    )
    asset = models.OneToOneField('Asset', related_name='parts_of_asset')
    parts_type = models.CharField(choices=PARTS_CHOICES, max_length=32)
    unit_price = models.FloatField(verbose_name=u'单价',blank=True,null=True)
    # total = models.IntegerField(verbose_name=u'总数',blank=True,null=True)
    used = models.IntegerField(verbose_name=u'已用',blank=True,null=True)
    rest = models.IntegerField(verbose_name=u'剩余',blank=True,null=True)
    specifications = models.CharField(verbose_name=u'规格',max_length=128,blank=True,null=True)
    # host = models.ForeignKey('Asset',related_name='parts_of_host',verbose_name=u'所属主机',blank=True,null=True,default=None)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='parts_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='parts_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'配件'
        verbose_name_plural = u'配件'


#机房
class IDC(models.Model):
    name = models.CharField(verbose_name=u'机房名称',max_length=64,unique=True)
    address = models.TextField(verbose_name=u'地址', null=True, blank=True)
    contact = models.ForeignKey(Contacts,verbose_name=u"联系人", null=True, blank=True)
    status = models.CharField(choices=SIMPLE_STATUS_CHOICES, verbose_name=u'状态',max_length=16, default='available')
    isself = models.CharField(verbose_name=u'自建/租借',choices=SELF_OR_LEASE_CHOICES,max_length=16, default='self')
    # contract = models.ManyToManyField(Contract, verbose_name=u'合同',null=True, blank=True)
    contract = models.ManyToManyField(Contract, verbose_name=u'合同') #null has no effect on ManyToManyField
    cost = models.FloatField(verbose_name=u'成本(元)',null=True, blank=True)
    start_date = models.DateField(verbose_name=u'起始时间',blank=True,null=True)
    end_date = models.DateField(verbose_name=u'结束时间',blank=True,null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='idc_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='idc_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'机房'
        verbose_name_plural = u"机房"

# 操作系统
class OS(models.Model):
    version = models.CharField(verbose_name=u'版本', max_length=128, unique=True)
    os_type = models.CharField(choices=OS_TYPE_CHOICES, verbose_name=u'系统类型', max_length=64, default='linux')
    soft_license = models.CharField(verbose_name=u'许可证', max_length=256, null=True, blank=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='os_create_user', null=True, blank=True)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='os_update_user', null=True, blank=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    def __unicode__(self):
        return self.version
    class Meta:
        verbose_name = u'操作系统'
        verbose_name_plural = u"操作系统"



#设备型号
# class ProductModel(models.Model):
#     name = models.CharField(verbose_name=u'设备型号', max_length=64,unique=True)
#     # manufactory = models.ForeignKey(Manufactory,verbose_name=u'厂商',null=True, blank=True)
#     manufactory = models.ForeignKey(Company,verbose_name=u'厂商',null=True, blank=True)
#     height = models.SmallIntegerField(verbose_name=u'设备高度', null=True, blank=True)
#     asset_type = models.CharField(verbose_name=u'设备类型',choices=ASSET_TYPE_CHOICES,max_length=64, default='server')
#     power = models.IntegerField(verbose_name=u'设备功率(W)',blank=True,null=True)
#     create_date = models.DateField(verbose_name=u'创建时间',auto_now_add=True)
#     update_date= models.DateField(verbose_name=u'更新时间',auto_now=True)
#     memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
#     class Meta:
#         verbose_name = u'设备型号'
#         verbose_name_plural = u"设备型号"
#     def __unicode__(self):
#         return self.name

# #资产类型
# class AssetType(models.Model):
#     name = models.CharField(verbose_name=u'类型名称', max_length=128, unique=True)
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name = u'资产类型'
#         verbose_name_plural = u'资产类型'

# 设备状态
# class AssetStatus(models.Model):
#     name = models.CharField(verbose_name=u'状态名称', max_length=64,unique=True)
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name = u'设备状态'
#         verbose_name_plural = u'设备状态'

#标签
# class Tag(models.Model):
#     name = models.CharField(verbose_name=u'标签名称',max_length=32,unique=True )
#     created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
#     createDate = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
#     update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
#     memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
#     def __unicode__(self):
#         return self.name
#     class Meta:
#         verbose_name = u'标签'
#         verbose_name_plural = u'标签'

#租用/借出
class Rent(models.Model):
    RENT_CHOICES = (
        ('from',u'租用'),
        ('to',u'借出'),
    )
    RENT_STATUS_CHOICES = (
        ('returned',u'归还'),
        ('notreturned',u'未归还'),
    )
    asset = models.ForeignKey('Asset')
    from_or_to = models.CharField(choices=RENT_CHOICES,verbose_name=u'租用/借出',max_length=64,default='to')
    receiver = models.CharField(verbose_name=u'接手人',max_length=64,null=True,blank=True)
    receiver_phone = models.CharField(verbose_name=u'接手人联系方式',max_length=64,null=True,blank=True)
    receiver_company = models.CharField(verbose_name=u'接手人单位',max_length=128,null=True,blank=True)
    handler = models.CharField(verbose_name=u'经办人',max_length=64,null=True,blank=True)
    handler_phone = models.CharField(verbose_name=u'经办人联系方式',max_length=64,null=True,blank=True)
    handler_company = models.CharField(verbose_name=u'经办人单位', max_length=128, null=True, blank=True)
    rent_date = models.DateField(verbose_name=u'起始时间',null=True,blank=True)
    rent_period = models.SmallIntegerField(verbose_name=u"租期",null=True, blank=True)
    returned_date = models.DateField(verbose_name=u'归还日期',null=True,blank=True)
    returned_status = models.CharField(choices=RENT_STATUS_CHOICES,verbose_name=u'归还/未归还',max_length=64,default='notreturned')
    usage = models.CharField(verbose_name=u'用途', max_length=256,null=True, blank=True)
    rent_cost = models.FloatField(verbose_name=u'租借成本',null=True, blank=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)


#新资产审批区
# class NewAssetApprovalZone(models.Model):
#     sn = models.CharField(verbose_name=u'序列号',max_length=128, unique=True)
#     asset_type = models.CharField(verbose_name=u'设备类型',choices=ASSET_TYPE_CHOICES,max_length=64,blank=True,null=True)
#     # asset_type = models.ForeignKey('AssetType', verbose_name=u'设备类型')
#     # manufacturer = models.CharField(verbose_name=u'厂商',max_length=64,blank=True,null=True)
#     model = models.CharField(verbose_name=u'型号',max_length=128,blank=True,null=True)
#     ram_size = models.IntegerField(blank=True,null=True)
#     cpu_model = models.CharField(max_length=128,blank=True,null=True)
#     cpu_count = models.IntegerField(blank=True,null=True)
#     # cpu_core_count = models.IntegerField(blank=True,null=True)
#     # os_type =  models.CharField(max_length=64,blank=True,null=True)
#     os_release =  models.CharField(max_length=64,blank=True,null=True)
#     data = models.TextField(verbose_name=u'资产数据')
#     date = models.DateTimeField(verbose_name=u'汇报日期',auto_now_add=True)
#     approved = models.BooleanField(verbose_name=u'已批准',default=False)
#     approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=u'批准人',blank=True,null=True)
#     approved_date = models.DateTimeField(verbose_name=u'批准日期',blank=True,null=True)
#
#     def __unicode__(self):
#         return self.sn
#     class Meta:
#         verbose_name = u'新上线待批准资产'
#         verbose_name_plural = u"新上线待批准资产"

