#_*_coding:utf-8_*_
from django.db import models
from itam import settings
# Create your models here.
from iuser.models import Departments
from info.models import Contract


LEVEL_CHOICES = (
    ('one',u'1级'),
    ('two',u'2级'),
    ('three',u'3级'),
    ('four',u'4级'),
    ('five',u'5级'),
)

TYPE_CHOICES = (
    ('parent',u'服务大类'),
    ('child',u'服务小类'),
    ('content',u'服务内容'),
)

STATUS_CHOICES = (
    ('online',u'已上线'),
    ('offline',u'已下线'),
)

#服务信息
class ServiceInfo(models.Model):
    parent_service = models.ForeignKey('self',related_name='parent_level',blank=True,null=True,verbose_name=u'父级服务')
    name = models.CharField(verbose_name=u'服务名称',max_length=64, unique=True)
    type = models.CharField(choices=TYPE_CHOICES,verbose_name=u'类型',max_length=64,default='parent')
    level = models.CharField(verbose_name=u'服务等级',choices=LEVEL_CHOICES, max_length=64,default='one')
    status = models.CharField(choices=STATUS_CHOICES, verbose_name=u'状态', max_length=64, default='online')
    contact = models.CharField(verbose_name=u'联系人',max_length=128,blank=True, null=True)
    department = models.ForeignKey(Departments, verbose_name=u'所属部门', blank=True, null=True)
    contract = models.ManyToManyField(Contract,verbose_name=u"相关合同")
    online_date = models.DateField(verbose_name=u'上线时间', blank=True, null=True)
    offline_date = models.DateField(verbose_name=u'下线时间', blank=True, null=True)
    create_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'创建人', related_name='serviceinfo_create_user', null=True, blank=True,default=None)
    update_person = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'最后更新人', related_name='serviceinfo_update_user', null=True, blank=True,default=None)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', null=True, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'服务'
        verbose_name_plural = u"服务"