#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response

# Create your views here.
from itam.api import *
from iservice import models
from iuser.models import Departments
from forms import ServiceForm
from iuser.models import User
from info.models import Contract
import copy

@require_role(role='user')
def service_index(request):
    """
    服务信息列表首页
    """
    header_title, path1, path2 = u'服务信息列表', u'服务信息', u'列表'

    return my_render('iservice/list.html', locals(), request)

@require_role(role='user')
def service_list(request):
    """
    服务信息列表
    """
    service_obj_all = models.ServiceInfo.objects.all()
    service_obj = service_obj_all
    filter_str = request.GET.get('filter')
    #关键字过滤
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("name"):
            service_obj = service_obj.filter(name__icontains=filter_dict["name"].strip())
        if filter_dict.has_key("level"):
            key = choice_code(models.LEVEL_CHOICES,filter_dict["level"])
            service_obj = service_obj.filter(level=key)
        if filter_dict.has_key("type"):
            key = choice_code(models.TYPE_CHOICES, filter_dict['type'])
            service_obj = service_obj.filter(type=key)
        if filter_dict.has_key("parent_service"):
            service_obj = service_obj.filter(parent_service__name__icontains=filter_dict['parent_service'])
        if filter_dict.has_key("status"):
            key = choice_code(models.STATUS_CHOICES,filter_dict["status"])
            service_obj = service_obj.filter(status=key)
        if filter_dict.has_key("department"):
            id = Departments.objects.get(name=filter_dict["department"]).id
            service_obj = service_obj.filter(department_id=id)
        if filter_dict.has_key("online_date"):
            service_obj = service_obj.filter(online_date=filter_dict["online_date"])
        if filter_dict.has_key("contact"):
            service_obj = service_obj.filter(contact__icontains=filter_dict["contact"])
        if filter_dict.has_key("memo"):
            service_obj = service_obj.filter(memo__icontains=filter_dict["memo"])
    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(service_obj, request)
    total = service_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        service = models.ServiceInfo.objects.get(name=r_dict['name'])
        r_dict['type'] = service.get_type_display()
        r_dict['status'] = service.get_status_display()
        r_dict['level'] = service.get_level_display()
        r_dict['department'] = '' if r_dict['department_id'] == None or r_dict['department_id'] == '' else Departments.objects.get(id=r_dict['department_id']).name
        r_dict['online_date'] = '' if r_dict['online_date'] == None else r_dict['online_date']  #如果为空，让前端啥都不显示，默认会显示“null”
        r_dict['offline_date'] = '' if r_dict['offline_date'] == None else r_dict['offline_date']
        if r_dict['parent_service_id'] != None and r_dict['parent_service_id'] != '':
            r_dict['parent_service'] = models.ServiceInfo.objects.get(id=r_dict['parent_service_id']).name
        else:
            r_dict['parent_service'] = ''
        if r_dict['create_person_id'] != None and r_dict['create_person_id'] != '':
            r_dict['create_person'] = User.objects.get(id=r_dict['create_person_id']).username
        else:
            r_dict['create_person'] = ''
        r_dict['update_person'] = '' if r_dict['update_person_id'] == None or r_dict['update_person_id'] == '' else User.objects.get(id=r_dict['update_person_id']).username
        rows_list.append(r_dict)

    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))

@require_role(role='user')
def service_add(request):
    """
    服务信息添加
    """
    level_choices = models.LEVEL_CHOICES
    type_choices = models.TYPE_CHOICES
    status_choices = models.STATUS_CHOICES
    department_choices = Departments.objects.all()
    parent_choices = models.ServiceInfo.objects.filter(type__in=["parent","child"])
    emg = ''    #error message
    smg = ''    #success message
    if request.method == 'POST':
        # postdata = request.POST
        current_user = User.objects.get(username=request.user.username)
        postdata = copy.deepcopy(request.POST)
        postdata["create_person"] = current_user.id
        postdata["update_person"] = current_user.id
        # service_form = ServiceForm(postdata,initial={"create_person":current_user,"update_person":current_user})
        service_form = ServiceForm(postdata)
        if service_form.is_valid():
            service_name = service_form.cleaned_data['name']
            service_obj = service_form.save(commit=False)
            try:
                contract_obj = Contract.objects.get(id=postdata['contract'])
            except Exception, e:
                print "服务信息中服务合同有可能为空：", e
            else:
                service_obj.contract.add(contract_obj)
            service_obj.save()
            smg = u'%s 添加成功' % service_name
        else:
            error = service_form.errors
            for e in error:
                emg += error[e].as_text().split("*")[1] + ";"
                # print dir(error[e])
            print 'error message:', emg
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iservice/add.html', locals(), request)

@require_role(role='user')
def service_edit(request):
    """
    服务信息编辑
    """
    level_choices = models.LEVEL_CHOICES
    type_choices = models.TYPE_CHOICES
    status_choices = models.STATUS_CHOICES
    department_choices = Departments.objects.all()
    emg = ''    #error message
    smg = ''    #success message
    if request.method == 'POST':
        # postdata = request.POST
        # print "POST:", postdata
        postdata = copy.deepcopy(request.POST)
        current_user = User.objects.get(username=request.user.username)
        postdata["update_person"] = current_user.id
        old_name = postdata.get("old_name")
        new_name = postdata.get("name")
        service_obj_old = models.ServiceInfo.objects.get(name=old_name)
        # service_obj_new = models.ServiceInfo.objects.get(name=postdata.get("name"))
        service_form = ServiceForm(postdata, instance=service_obj_old)
        if old_name != new_name and models.ServiceInfo.objects.filter(name=postdata.get("name")):
            emg = u'修改失败，%s 已存在' % postdata.get("name")
        else:
            if service_form.is_valid():
                service_obj = service_form.save(commit=False)
                try:
                    contract_obj = Contract.objects.get(id=postdata['contract'])
                except Exception, e:
                    print "服务信息中服务合同有可能为空：", e
                else:
                    service_obj.contract.add(contract_obj)
                service_obj.save()
                smg = u'%s 修改成功' % postdata.get("old_name")
            else:
                error = service_form.errors
                for e in error:
                    emg += error[e].as_text().split("*")[1] + ";"
                print 'error message:', emg
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    if request.method == 'GET':
        service_name = request.GET['name']
        parent_choices = models.ServiceInfo.objects.exclude(name=service_name)
        try:
            service_detail = models.ServiceInfo.objects.get(name=service_name)
        except Exception,e:
            emg = u'更新失败, 此服务 %s 不存在!' % service_name
        return my_render('iservice/edit.html', locals(), request)

@require_role(role='super')
def service_delete(request):
    """
    服务信息删除
    """
    smg = []  # success message
    emg = []  # error message
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "service_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    service_select = models.ServiceInfo.objects.get(id=i)
                    service_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功" % service_select.name)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))