#_*_coding:utf-8_*_
from django.db import models

# Create your models here.
from iasset.models import Asset
from iuser.models import User

#事件日志
class EventLog(models.Model):
    # name = models.CharField(u'事件名称', max_length=100)
    EVENT_TYPE_CHOICES = (
        ('add',u'增加'),
        ('delete',u'删除'),
        ('change',u'更改'),
        ('login',u'登录'),
    )
    eventtype = models.CharField(u'事件类型', choices=EVENT_TYPE_CHOICES ,max_length=64)
    # eventType = models.CharField(verbose_name=u'事件类型', max_length=128)
    target = models.CharField(verbose_name=u'操作对象', max_length=128)
    user = models.ForeignKey(User, verbose_name=u'用户')
    remote_ip = models.CharField(verbose_name=u'登录IP', max_length=100, blank=True, null=True)
    # asset = models.ForeignKey(Asset)
    # component = models.CharField(verbose_name='事件子项',max_length=255, blank=True,null=True)
    date = models.DateTimeField(verbose_name=u'日期', auto_now_add=True)
    detail = models.TextField(verbose_name=u'事件详情')
    # memo = models.TextField(verbose_name=u'备注',blank=True,null=True)
    # def __unicode__(self):
    #     return self.name
    class Meta:
        verbose_name = u'事件日志'
        verbose_name_plural = u"事件日志"