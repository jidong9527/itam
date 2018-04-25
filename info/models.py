#_*_coding:utf-8_*_
__author__ = 'jidong'

from django.db import models
from iasset.share import ASSET_TYPE_CHOICES
from itam import settings
# from iasset.tests import ProductModel
# import iasset
# Create your models here.


#联系人
class Contacts(models.Model):
    name = models.CharField(verbose_name=u'姓名',max_length=64, unique=True)
    phone_number = models.CharField(verbose_name=u'电话',max_length=30,blank=True,null=True)
    email = models.EmailField(verbose_name=u'邮箱',blank=True,null=True)
    company = models.ForeignKey('Company', verbose_name=u'公司')
    position = models.CharField(verbose_name=u'职位', max_length=64, blank=True, null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='contacts_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='contacts_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'联系人'
        verbose_name_plural = u"联系人"

#供应商/厂商
# class Supplier(models.Model):
class Company(models.Model):
    name = models.CharField(verbose_name=u'公司名称',max_length=64, unique=True)
    # contact = models.ForeignKey('Contacts',verbose_name="联系人",default=None,blank=True,null=True)
    address = models.CharField(verbose_name=u'公司地址', max_length=256, blank=True, null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='company_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='company_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    def __unicode__(self):
        return self.manufactory
    class Meta:
        verbose_name = u'供应商/厂商'
        verbose_name_plural = u"供应商/厂商"

#厂商
# class Manufactory(models.Model):
#     name = models.CharField(verbose_name=u'厂商名称',max_length=64, unique=True)
#     contact = models.ForeignKey('Contacts',verbose_name="联系人",default=None,blank=True,null=True)
#     create_date = models.DateField(verbose_name=u'创建时间',auto_now_add=True)
#     update_date= models.DateField(verbose_name=u'更新时间',auto_now=True)
#     memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
#     def __unicode__(self):
#         return self.manufactory
#     class Meta:
#         verbose_name = u'厂商'
#         verbose_name_plural = u"厂商"

#合同
class Contract(models.Model):
    name = models.CharField(verbose_name=u'合同名称', max_length=64,unique=True)
    sn = models.CharField(verbose_name=u'合同编号', max_length=128,blank=True,null=True)
    company = models.ForeignKey('Company',verbose_name=u'供应商')
    # supplier = models.ForeignKey('Supplier',verbose_name=u'供应商')
    cost = models.FloatField(verbose_name=u'费用',blank=True,null=True)
    project = models.ForeignKey('Project',verbose_name=u'所属项目')
    start_date = models.DateField(verbose_name=u'起始时间', blank=True,null=True)
    end_date = models.DateField(verbose_name=u'结束时间',blank=True,null=True)
    pdf = models.FileField(verbose_name=u'电子版合同', upload_to='contract/', blank=True, null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='contract_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='contract_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True,null=True)
    class Meta:
        verbose_name = u'合同'
        verbose_name_plural = u'合同'
    def __unicode__(self):
        return self.name

#合同采购的设备
class DeviceOfContract(models.Model):
    model = models.ForeignKey('ProductModel', verbose_name=u'设备型号')
    # model = models.CharField(verbose_name=u'设备型号', max_length=128, unique=True)
    contract = models.ForeignKey('Contract', verbose_name=u'所属合同')
    cpu_count = models.SmallIntegerField(verbose_name=u'CPU个数', blank=True, null=True)
    cpu_model = models.CharField(verbose_name=u'CPU型号', max_length=128, blank=True, null=True)
    ram = models.FloatField(verbose_name=u'内存大小(G)', blank=True, null=True)
    disk = models.FloatField(verbose_name=u'磁盘容量(G)', blank=True, null=True)
    price = models.FloatField(verbose_name=u'价格', blank=True, null=True)
    quantity = models.IntegerField(verbose_name=u'设备数量', blank=True, null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='doc_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='doc_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True)
    class Meta:
        verbose_name = u'合同采购的设备'
        verbose_name_plural = u'合同采购的设备'
    def __unicode__(self):
        return self.name

#项目
class Project(models.Model):
    name = models.CharField(verbose_name=u'项目名称',max_length=128,unique=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='project_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='project_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True,null=True)
    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'
    def __unicode__(self):
        return self.name

#设备型号
class ProductModel(models.Model):
    name = models.CharField(verbose_name=u'设备型号', max_length=256,unique=True)
    # manufactory = models.ForeignKey(Manufactory,verbose_name=u'厂商',null=True, blank=True)
    manufactory = models.ForeignKey('Company',verbose_name=u'厂商',null=True, blank=True)
    height = models.SmallIntegerField(verbose_name=u'设备高度', null=True, blank=True)
    asset_type = models.CharField(verbose_name=u'设备类型',choices=ASSET_TYPE_CHOICES,max_length=64, default='server')
    power = models.IntegerField(verbose_name=u'设备功率(W)',blank=True,null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='pm_create_user', null=True, blank=True, default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='pm_update_user', null=True, blank=True,default=None)
    # create_date = models.DateField(verbose_name=u'创建时间',auto_now_add=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    # update_date = models.DateTimeField(verbose_name=u'更新时间',default=timezone.now())
    update_date = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    class Meta:
        verbose_name = u'设备型号'
        verbose_name_plural = u"设备型号"
    def __unicode__(self):
        return self.name