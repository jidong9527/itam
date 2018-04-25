#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response
from itam.api import *
from iasset.share import ASSET_TYPE_CHOICES
from info import models
import json
from django.utils import timezone
# Create your views here.

def contacts(request):
    header_title, path1, path2 = u'联系人', u'信息', u'联系人'
    return my_render('info/contacts/list.html', locals(), request)

def contract(request):
    header_title, path1, path2 = u'合同', u'信息', u'合同'
    return my_render('info/contract/list.html', locals(), request)

# def manufacturers(request):
#     return render_to_response('info/info_manufacturers.html')

def project(request):
    header_title, path1, path2 = u'项目', u'信息', u'项目'
    return my_render('info/project/list.html', locals(), request)

def company(request):
    header_title, path1, path2 = u'供应商/厂商', u'信息', u'商家'
    company_list = models.Company.objects.all()
    return my_render('info/company/list.html', locals(), request)

def company_add(request):
    """
    添加供应商/厂商
    :param request:
    :return:
    """
    header_title, path1, path2 = u'供应商/厂商', u'信息', u'商家'
    if request.method == "POST":
        print request.POST
        company = request.POST.get("company")
        address = request.POST.get("address","")
        contact = request.POST.get("contact","")
        phone = request.POST.get("phone","")
        memo = request.POST.get("memo","")
        try:
            if models.Company.objects.filter(name=unicode(company)):
                emg = u"添加失败，该公司名称 %s 已存在" % company
                raise ServerError(emg)
        except ServerError:
            pass
        else:
            models.Company.objects.create(name=company,address=address,memo=memo)
            smg = "添加成功"
    source_url = request.META.get("HTTP_REFERER")
    print source_url
    return my_render('info/company/add.html', locals(), request)

def manage_models(request):
    """
    设备类型管理
    """
    header_title, path1, path2 = u'设备型号管理', u'资产', u'管理'
    models_list_all = models.ProductModel.objects.all()
    manufactory_select = models.Company.objects.all()

    # return my_render('iasset/manage/models/list.html', json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder), request)
    return my_render('iasset/manage/models/list.html', locals(), request)

def manage_models_list(request):
    """
    设备类型列表
    返回json格式数据
    """
    models_obj_all = models.ProductModel.objects.all()
    filter_str = request.GET.get('filter')
    models_obj = models_obj_all
    # print "filter_str type:",type(filter_str)
    if filter_str:
        filter_dict = eval(filter_str)
        # print filter_dict
        # print "filter_dict:",type(filter_dict)
        # print "filter not null"
        # print 'filter:',filter_dict
        if filter_dict.has_key("name"):
            models_obj = models_obj.filter(name__icontains=filter_dict["name"].strip())  #包含、忽略大小写
        if filter_dict.has_key("manufactory"):
            models_obj = models_obj.filter(manufactory__name=filter_dict["manufactory"]) #等于
        if filter_dict.has_key("height"):
            models_obj = models_obj.filter(height=filter_dict["height"])
        if filter_dict.has_key("asset_type"):
            print filter_dict["asset_type"],type(filter_dict["asset_type"])
            for k,v in dict(ASSET_TYPE_CHOICES).iteritems():
                if v.encode("utf-8") == filter_dict["asset_type"]:
                    asset_type_key = k
            print "asset_type_key:",asset_type_key
            models_obj = models_obj.filter(asset_type=asset_type_key)
        if filter_dict.has_key("power"):
            models_obj = models_obj.filter(power=filter_dict["power"])
        if filter_dict.has_key("memo"):
            models_obj = models_obj.filter(memo__icontains=filter_dict["memo"])

    else:
        print "filter is null"
        # models_obj = models_obj_all

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(models_obj, request)
    total = models_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        models_filter = models.ProductModel.objects.get(name=r_dict['name'])
        r_dict['asset_type'] = models_filter.get_asset_type_display()
        if r_dict['manufactory_id'] != None and r_dict['manufactory_id'] != "":
            r_dict['manufactory'] = models_filter.manufactory.name
        else:
            r_dict['manufactory'] = ""
        rows_list.append(r_dict)

    print "rows_list:",rows_list

    return HttpResponse(json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder))


def manage_models_add(request):
    """
    设备类型添加页面
    """
    header_title, path1, path2 = u'添加设备类型', u'资产', u'管理'
    asset_types = ASSET_TYPE_CHOICES
    manufactory_select = models.Company.objects.all()
    emg = ""  #error message
    smg = ""  #success message

    if request.method == "GET":
        return my_render('iasset/manage/models/add.html', locals(), request)

    if request.method == "POST":
        print request.POST
        modelname = request.POST.get("modelname", "")
        manufactory = request.POST.get("manufactory")
        height1 = request.POST.get("height", 0)
        height = 0 if height1=="" else height1
        # print "heigt:",height,type(height)
        asset_type = request.POST.get("assettype", "")
        power1 = request.POST.get("power", 0)
        power = 0 if power1=="" else power1
        # print "power:",power,type(power)
        memo = request.POST.get("memo","")
        if manufactory == '':
            manufactory = None
        try:
            if models.ProductModel.objects.filter(name=unicode(modelname)):
                emg = u"添加失败，该设备型号 %s 已存在" % modelname
                raise ServerError(emg)
        except ServerError:
            pass
        else:
            models.ProductModel.objects.create(name=modelname, manufactory_id=manufactory, height=height, asset_type=asset_type, power=power, memo=memo)
            smg = u"%s 添加成功" % modelname
        return HttpResponse(json.dumps({"smg":smg,"emg":emg}))
@require_role(role='super')
def manage_models_del(request):
    """
    删除机器型号
    """
    print request.method
    if request.method == "POST":
        # post_data = request.POST
        # batch = request.GET.get('batch')
        id_select = request.POST.getlist("id_select",[])
        print "id_select:",id_select,type(id_select)
        if id_select:
            for i in id_select:
                print models.ProductModel.objects.filter(id=i)
                models.ProductModel.objects.filter(id=i).delete()
    return HttpResponse(u"删除成功")

def manage_models_edit(request):
    """
    编辑型号页面
    """
    header_title, path1, path2 = u'编辑设备类型', u'资产', u'管理'
    asset_types = ASSET_TYPE_CHOICES
    manufactory_select = models.Company.objects.all()
    smg = '' #success message
    emg = '' #error message
    if request.method == "GET":
        models_name = request.GET["name"]
        try:
            models_detail = models.ProductModel.objects.get(name=models_name)
        except Exception, e:
            emg = u"该型号不存在"
        return my_render('iasset/manage/models/edit.html', locals(), request)

    if request.method == "POST":
        print "POST data:",request.POST
        model_name = request.POST.get("modelname", "")
        manufactory = request.POST.get("manufactory")
        height1 = request.POST.get("height", 0)
        height = 0 if height1=="" else height1
        # print "heigt:",height,type(height)
        asset_type = request.POST.get("assettype", "")
        power1 = request.POST.get("power", 0)
        power = 0 if power1=="" else power1
        # print "power:",power,type(power)
        memo = request.POST.get("memo","")
        if manufactory == '':
            manufactory = None
        try:
            models_detail = models.ProductModel.objects.filter(name=model_name)
            print models_detail
        except Exception, e:
            emg = u"该型号不存在,",e
        else:
            try:
                models_detail.update(manufactory_id=manufactory, height=height, asset_type=asset_type, power=power, memo=memo, update_date=timezone.now())
            except Exception, e:
                emg = u"错误:",e
            else:
                smg = u"更新成功！"
        return HttpResponse(json.dumps({"smg":smg,"emg":emg}))

def manage_models_detail(request):
    """
    型号详情
    """
    header_title, path1, path2 = u'设备型号详情', u'资产', u'管理'
    if request.method == "GET":
        models_id = request.GET["id"]
        try:
            models_detail = models.ProductModel.objects.get(id=models_id)
            print models_detail.get_asset_type_display()
        except Exception,e:
            emg = u"该型号不存在"
        print models_detail.update_date
        print models_detail.create_date

    return my_render('iasset/manage/models/detail.html', locals(), request)
