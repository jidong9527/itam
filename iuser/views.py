#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response
from itam.api import *
from iuser import models
# Create your views here.

def user(request):
    header_title, path1, path2 = u'用户列表', u'用户', u'用户列表'
    return my_render('iuser/user/list.html', locals(), request)

def user_list(request):
    emg = ""  #error message
    smg = ""  #success message
    active_dict = {'True':u'激活','False':u'禁用'}
    user_obj_all = models.User.objects.all()
    filter_str = request.GET.get('filter')
    user_obj = user_obj_all
    if filter_str:
        filter_dict = eval(filter_str)
    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(user_obj, request)
    total = user_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        models_filter = models.User.objects.get(username=r_dict['username'])
        r_dict['role'] = models_filter.get_role_display()
        print models_filter.is_active
        print active_dict
        r_dict['is_active'] = active_dict[str(models_filter.is_active)]
        rows_list.append(r_dict)

    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))

def user_add(request):
    header_title, path1, path2 = u'添加用户', u'用户', u'添加用户'
    emg = ''
    smg = ''
    role_choice = models.User.USER_ROLE_CHOICES
    group_all = models.UserGroup.objects.all()
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('username','')
        name = request.POST.get('name','')
        role = request.POST.get('role','cu')
        is_active = request.POST.get('is_active',True)
        group = request.POST.get('group',None)
        department = request.POST.get('department',None)
        memo = request.POST.get('memo','')
        if group == '':
            group = None
        if department == '':
            department = None
        try:
            if '' in [username, password]:
                emg = u'带*内容不能为空'
                raise ServerError
            check_user_is_exist = models.User.objects.filter(username=username)
            if check_user_is_exist:
                emg = u'用户 %s 已存在' % username
                raise ServerError

        except ServerError:
            pass
        else:
            try:
                user = models.User(username=username,password=password,
                            role=role,is_active=is_active,name=name,
                            department_id=department,memo=memo)
                user.set_password(password)
                user.save()
                user.group.add(group)
            except IndexError, e:
                emg = u'添加用户 %s 失败 %s ' % (username, e)
        return HttpResponse(json.dumps({"smg":smg,"emg":emg}))

    return my_render('iuser/user/add.html', locals(), request)

def user_edit(request):
    header_title, path1, path2 = u'修改用户', u'用户', u'修改用户'
    pass
@require_role(role='super')
def user_delete(request):
    pass

def group(request):
    header_title, path1, path2 = u'用户组列表', u'用户组', u'用户组列表'
    return my_render('iuser/group/list.html', locals(), request)

def group_list(request):
    total = []
    rows_list = []
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))

def group_add(request):
    header_title, path1, path2 = u'添加用户组', u'用户组', u'添加用户组'
    pass
def group_edit(request):
    header_title, path1, path2 = u'修改用户组', u'用户组', u'修改用户组'
    pass
@require_role(role='super')
def group_delete(request):
    pass
@require_role(role='super')
def departments(request):
    header_title, path1, path2 = u'部门列表', u'用户', u'部门列表'
    return my_render('iuser/department/list.html', locals(), request)
@require_role(role='super')
def departments_list(request):
    """
    部门信息列表
    """
    departments_obj_all = models.Departments.objects.all()
    filter_str = request.GET.get('filter')
    departments_obj = departments_obj_all
    # 关键字过滤
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("name"):
            departments_obj = departments_obj.filter(name__icontains=filter_dict["name"].strip())
        if filter_dict.has_key("memo"):
            departments_obj = departments_obj.filter(memo__icontains=filter_dict["memo"].strip())

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(departments_obj, request)
    total = departments_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        rows_list.append(r_dict)
    print "rows_list:", rows_list
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='super')
def departments_add(request):
    """
    添加部门
    """
    header_title, path1, path2 = u'添加部门', u'用户', u'添加部门'
    emg = ""  # error message
    smg = ""  # success message
    if request.method == "POST":
        print "request.POST:", request.POST
        post_name = request.POST.get('name')
        post_memo = request.POST.get('memo')
        if models.Departments.objects.filter(name=post_name):
            emg = u'添加失败, %s 已存在!' % post_name
        else:
            deppost = models.Departments(name=post_name,memo=post_memo)
            deppost.save()
            smg = u'%s 添加成功' % post_name
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iuser/department/add.html', locals(), request)
@require_role(role='super')
def departments_edit(request):
    """
    编辑部门
    """
    header_title, path1, path2 = u'编辑部门', u'用户', u'编辑部门'
    emg = ""  # error message
    smg = ""  # success message
    if request.method == "GET":
        get_name = request.GET['name']
        department_detail = models.Departments.objects.get(name=get_name)
    if request.method == "POST":
        print "request.POST:", request.POST
        post_name = request.POST.get('name')
        post_old_name = request.POST.get('old_name')
        post_memo = request.POST.get('memo')
        deppost = models.Departments.objects.filter(name=post_name)
        deppost_old = models.Departments.objects.get(name=post_old_name)
        if deppost and post_name != post_old_name:   #如果修改部门名称，先查看修改后的名称是否已经存在
            emg = u'编辑失败, %s 已存在!' % post_name
        else:
            deppost_old.name = post_name
            deppost_old.memo = post_memo
            deppost_old.save()
            smg = u'%s 修改成功' % post_old_name
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iuser/department/edit.html', locals(), request)
@require_role(role='super')
def departments_delete(request):
    """
       删除部门
       """
    # header_title, path1, path2 = u'删除机房', u'资产', u'机房'
    smg = []  # success message
    emg = []  # error message
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "idc_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    departments_select = models.Departments.objects.get(id=i)
                    departments_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功\n" % departments_select.name)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))