#_*_coding:utf-8_*_

from django import template
register = template.Library()

@register.filter(name='strip_space')
def strip_space(string):
    """
    去掉字符串两边的空格
    :param string:
    :return:
    """
    return string.strip()

@register.filter(name='to_name')
def to_name(user_id):
    """user id 转位用户名称"""
    try:
        user = User.objects.filter(id=int(user_id))
        if user:
            user = user[0]
            return user.name
    except:
        return '非法用户'

@register.filter(name='get_role')
def get_role(user_id):
    """
    根据用户id获取用户权限
    """
    user_role = {'su': u'超级管理员', 'cu': u'普通用户'}
    user = get_object(User, id=user_id)
    if user:
        return user_role.get(str(user.role), u"普通用户")
    else:
        return u"普通用户"