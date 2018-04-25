#_*_coding:utf-8_*_

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser



class UserGroup(models.Model):
    name = models.CharField(verbose_name=u'组名',max_length=80, unique=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date= models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True, default=None)

    def __unicode__(self):
        return self.name


class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('su', '超级用户'),
        # ('GA', 'GroupAdmin'),
        ('cu', '普通用户'),
    )
    name = models.CharField(verbose_name=u'姓名',max_length=80, blank=True, null=True)
    role = models.CharField(verbose_name=u'角色',max_length=2, choices=USER_ROLE_CHOICES, default='cu')
    group = models.ManyToManyField(UserGroup)
    department = models.ForeignKey('Departments', verbose_name=u'所属部门', default=None, blank=True, null=True)
    # is_active = models.BooleanField(verbose_name=u'激活',default=True)
    # last_login = models.DateTimeField(verbose_name=u'最后登录时间',null=True)
    # date_joined = models.DateTimeField(verbose_name=u'创建时间',null=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(verbose_name=u'备注', blank=True, null=True, default=None)

    def __unicode__(self):
        return self.username


# class AdminGroup(models.Model):
#     """
#     under the user control group
#     用户可以管理的用户组，或组的管理员是该用户
#     """
#
#     user = models.ForeignKey('User')
#     group = models.ForeignKey('UserGroup')
#
#     def __unicode__(self):
#         return '%s: %s' % (self.user.username, self.group.name)

class Departments(models.Model):
    name = models.CharField(verbose_name=u'部门名称',max_length=128,unique=True)
    create_date = models.DateTimeField(verbose_name=u'创建时间',auto_now_add=True)
    update_date = models.DateTimeField(verbose_name=u'更新时间',auto_now=True)
    memo = models.TextField(u'备注', blank=True, null=True, default=None)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'部门信息'
        verbose_name_plural = u"部门信息"