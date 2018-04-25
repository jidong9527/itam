#_*_coding:utf-8_*_
__author__ = 'jidong'


from django.db.models import Q

# Create your views here.
from itam.api import *
from iasset import models
from iasset.forms import *
from info.models import ProductModel,Contract
from iuser.models import User
from iservice.models import ServiceInfo
from ilog.models import EventLog
from inetwork.models import IPAddress, Ports
import copy

@require_role(role='user')
def asset_index(request):
    """
    资产列表首页
    """
    header_title, path1, path2 = u'资产列表', u'资产', u'列表'
    idc_all = models.IDC.objects.all()
    asset_types = models.ASSET_TYPE_CHOICES
    asset_status = models.DEVICE_STATUS
    return my_render('iasset/asset/list.html', locals(), request)

def asset_list(request):
    """
    资产列表
    :param request:
    :return:
    """
    asset_obj_all = models.Asset.objects.all()
    asset_obj = asset_obj_all
    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(asset_obj, request)
    total = asset_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        asset_select = models.Asset.objects.get(id=r_dict['id'])
        r_dict['asset_type'] = ProductModel.objects.get(id=asset_select.model_id).get_asset_type_display()
        r_dict['asset_type_key'] = ProductModel.objects.get(id=asset_select.model_id).asset_type
        r_dict['status'] = asset_select.get_status_display()
        r_dict['ip'] = ''
        ports = asset_select.ports_set.all()
        if ports.count() > 0:
            for i in ports:
                r_dict['ip'] += str(i.ip.ipaddress) + ';'
        cabinet_obj = get_device_attr(asset_select, r_dict['asset_type_key'], "cabinet")
        if cabinet_obj != '' and cabinet_obj != None:
            r_dict['cabinet'] = cabinet_obj.location
            r_dict['idc'] = cabinet_obj.idc.name
        else:
            r_dict['cabinet'] = ''
        service_obj = get_device_attr(asset_select, r_dict['asset_type_key'], "service")
        # print service_obj
        if service_obj != '' and service_obj != None:
            r_dict['service'] = service_obj.name
        else:
            r_dict['service'] = ''
        rows_list.append(r_dict)
    print "rows_list:",rows_list
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))

# def get_cabinet(asset_obj,asset_type):
#     """
#     根据资产名称返回机柜对象
#     """
#     asset_obj = asset_obj
#     asset_type = asset_type
#     if asset_type not in ["parts"]:
#         cabinet = eval("asset_obj.%s.cabinet" % asset_type)
#         return cabinet
#     else:
#         return ''

def get_device_attr(asset_obj,asset_type,attribute):
    """
    根据设备对象返回设备属性
    """
    # asset_obj = asset_obj
    # asset_type = asset_type
    # attr = attribute
    # if asset_type not in ["parts"]:
    #     ret = eval("asset_obj.%s.%s" % (asset_type,attribute))
    #     return ret
    # else:
    #     return ''
    # type_dict = {
    #      'server':  "server",
    #      'bladecenter':  u'刀箱',
    #      'blade':  u'刀片',
    #      'vm':  u'虚拟机',
    #      'network':  u'网络设备',
    #      'storage':  u'存储设备',
    #      'tape':  u'带库'  ,
    #      'security':  u'安全设备',
    #      'parts':  u'配件'  ,
    #      'others':  u'其它类',
    # }
    ret = eval("asset_obj.%s.%s" % (asset_type, attribute))
    return ret

@require_role(role='user')
def asset_add(request):
    """
    添加资产
    """

    header_title, path1, path2 = u'添加', u'资产', u'添加'
    emg = ''
    smg = ''
    asset_types = models.ASSET_TYPE_CHOICES  #设备类型
    asset_status = models.DEVICE_STATUS      #设备状态
    asset_contract = Contract.objects.all()  #合同
    cabinet_all = models.Cabinet.objects.all()  #机柜
    service_all = ServiceInfo.objects.all()     #服务
    os_all = models.OS.objects.all()            #操作系统
    current_user = User.objects.get(username=request.user.username)  #当前登录用户
    bladecenter_all = models.BladeCenter.objects.all()
    # hosts_all = Asset.objects.select_related().all()

    if request.method == 'GET':
        asset_type = request.GET['asset_type']
        modals_all = ProductModel.objects.filter(asset_type=asset_type)
        include_html = 'iasset/asset/add/%s.html' % asset_type
        if asset_type == 'vm':
            hosts_all = Asset.objects.filter(model__asset_type="server")
        elif asset_type == 'blade':
            hosts_all = Asset.objects.filter(model__asset_type="bladecenter")
        else:
            hosts_all = Asset.objects.filter(Q(model__asset_type="server") | Q(model__asset_type="bladecenter"))
        # print "asset_type:", asset_type
        # print "modals_all:", modals_all
        # print "service_all:", service_all
        # print "cabinet_all:", cabinet_all
    if request.method == 'POST':
        # postdata = request.POST
        postdata = copy.deepcopy(request.POST)    #深复制才能修改postdata的值
        print "POST:", postdata
        print "type(request.POST):", type(postdata)
        print "request.session:",request.session
        # postdata['create_person'] = current_user.id
        # postdata['update_person'] = current_user.id
        asset_form = AssetForm(postdata)
        # print 'asset_form:',asset_form
        if asset_form.is_valid():
            asset_name = asset_form.cleaned_data['name']
            if models.Asset.objects.filter(name=asset_name):
                emg = u'添加失败, 此设备 %s 已存在!' % asset_name
            else:
                asset_obj = asset_form.save(commit=False)
                try:
                    # 由于asset和contract之间是多对多关系，默认不能为空，所以要单拿出来添加，
                    # 如果提交的数据中contract为空，那么不添加该字段到数据库。
                    # 在forms.py 验证时已将contract字段排除
                    contract_obj = Contract.objects.get(id=postdata['contract'])
                except Exception,e:
                    print e
                else:
                    asset_obj.contract.add(contract_obj)
                asset_obj.create_person = current_user
                asset_obj.update_person = current_user
                asset_obj.save()
                asset_type = postdata['assettype']
                # init = {'asset': models.Asset.objects.get(name=asset_name)}
                print "asset_obj:",asset_obj.id
                # init = {'asset_id': asset_obj.id}
                postdata['asset'] = asset_obj.id
                # serverformset = ServerForm(postdata, initial=init)
                # if serverformset.is_valid():
                #     serverformset.save()
                # else:
                #     emg = serverformset.errors.as_json()
                ret = device_save(asset_type,postdata)
                if ret['status'] == 0:
                    smg = u'设备: %s添加成功' % asset_name
                else:
                    emg = ret['emg']
        else:
            # emg = asset_form.non_field_errors()
            emg = asset_form.errors.as_json()
            print 'error message:',emg
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iasset/asset/add/index.html', locals(), request)
def device_save(asset_type, postdata):
    """
     设备入库
    :param asset_type:
    :return:
    """
    asset_type_dict = {
        'server': ServerForm(postdata),
        'bladecenter': BladeCenterForm(postdata),
        'blade': BladeForm(postdata),
        'vm': VmForm(postdata),
        'network': NetworkForm(postdata),
        'storage': StorageForm(postdata),
        'tape': TapeForm(postdata),
        'security': SecurityForm(postdata),
        'parts': PartsForm(postdata),
        'others': OthersForm(postdata),
    }
    asset_type_form = asset_type_dict[asset_type]
    # print "asset_type_form", asset_type_form
    if asset_type_form.is_valid():
        asset_type_form.save()
        ret = {"status": 0, "smg":u"添加成功"}
    else:
        emg = asset_type_form.errors.as_json()
        print "error message: ",emg
        ret = {"status": 1, "emg": emg}
    return ret


@require_role(role='user')
def asset_add_alltype(request,arg1):
    """
    iasset/asset/add.html,选择资产类型，出现对应属性填写框
    """
    html = 'iasset/asset/add/%s' % arg1
    return my_render(html, locals(), request)
@require_role(role='user')
def asset_add_batch(request):
    header_title, path1, path2 = u'批量添加', u'资产', u'批量添加'
    return my_render('iasset/asset/add/batch.html', locals(), request)

@require_role(role='user')
def asset_delete(request):
    """资产删除"""
    smg = []  # success message
    emg = []  # error message
    print u"开始删除..."
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "asset_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    asset_select = models.Asset.objects.get(id=i)
                    asset_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功\n" % asset_select.name)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))


@require_role(role='user')
def asset_detail(request):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    if request.method == 'GET':
        asset_name = request.GET['asset_name']
        asset_type = request.GET['asset_type']
        print "request.GET:",request.GET
        print "asset_type:",asset_type
        viewname = 'asset_detail_%s' % asset_type
        print viewname
        # print reverse("asset_detail_blade",kwargs={'name':asset_name},)
        return HttpResponseRedirect(reverse(viewname,kwargs={'asset_name':asset_name}))
    # return my_render('iasset/asset/detail/index.html', locals(), request)

@require_role(role='user')
def asset_detail_blade(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    asset_obj = models.Asset.objects.get(name=asset_name)
    asset_type = ProductModel.objects.get(relatedmodel__name=asset_name)
    bladecenter_obj = models.BladeCenter.objects.all()
    model = models.ProductModel.objects.filter(asset_type="blade")
    # cabinet_all = models.Cabinet.objects.all()
    os_all = models.OS.objects.all()
    status_all = models.DEVICE_STATUS
    service_all = ServiceInfo.objects.filter(type="content")
    storagespace_all = models.StorageSpace.objects.all()
    return my_render('iasset/asset/detail/blade/index.html', locals(), request)

@require_role(role='user')
def asset_detail_bladecenter(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    asset_obj = models.Asset.objects.get(name=asset_name)
    asset_type = ProductModel.objects.get(relatedmodel__name=asset_name)
    model = models.ProductModel.objects.filter(asset_type="bladecenter")
    cabinet_all = models.Cabinet.objects.all()
    status_all = models.DEVICE_STATUS
    service_all = ServiceInfo.objects.filter(type="content")
    return my_render('iasset/asset/detail/bladecenter/index.html', locals(), request)

@require_role(role='user')
def asset_detail_network(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    asset_obj = models.Asset.objects.get(name=asset_name)
    asset_type = ProductModel.objects.get(relatedmodel__name=asset_name)
    model = models.ProductModel.objects.filter(asset_type="network")
    cabinet_all = models.Cabinet.objects.all()
    # os_all = models.OS.objects.all()
    status_all = models.DEVICE_STATUS
    service_all = ServiceInfo.objects.filter(type="content")
    # storagespace_all = models.StorageSpace.objects.all()
    return my_render('iasset/asset/detail/network/index.html', locals(), request)

@require_role(role='user')
def asset_detail_others(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/others/index.html', locals(), request)

@require_role(role='user')
def asset_detail_parts(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/parts/index.html', locals(), request)

@require_role(role='user')
def asset_detail_security(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/security/index.html', locals(), request)

@require_role(role='user')
def asset_detail_server(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    asset_obj = models.Asset.objects.get(name=asset_name)
    asset_type = ProductModel.objects.get(relatedmodel__name=asset_name)
    model = models.ProductModel.objects.filter(asset_type="server")
    cabinet_all = models.Cabinet.objects.all()
    os_all = models.OS.objects.all()
    status_all = models.DEVICE_STATUS
    service_all = ServiceInfo.objects.filter(type="content")
    storagespace_all = models.StorageSpace.objects.all()
    return my_render('iasset/asset/detail/server/index.html', locals(), request)

@require_role(role='user')
def asset_detail_storage(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/storage/index.html', locals(), request)

@require_role(role='user')
def asset_detail_tape(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/tape/index.html', locals(), request)

@require_role(role='user')
def asset_detail_vm(request,asset_name):
    header_title, path1, path2 = u'资产详情', u'资产', u'详细信息'
    return my_render('iasset/asset/detail/vm/index.html', locals(), request)

@require_role(role='user')
def asset_detail_item_action(request,asset_type,asset_name,item,action):
    """
    设备端口列表
    :param request:
    :param asset_type:  设备类型
    :param asset_name:  设备名称
    :itam:              要更改的栏目   ports、parts、contract、history...
    :action:            执行的动作     list、add、edit、delete
    :return:            total，rows
    """
    func = 'asset_detail_%s_%s' % (item,action)
    return eval(func)(request,asset_type,asset_name)      #调用函数，这里要用return ，不然返回值为None

@require_role(role='user')
def asset_detail_ports_list(request,asset_type,asset_name):
    """
    设备端口列表
    :param request:
    :param asset_type:  设备类型
    :param asset_name:  设备名称
    :return:            total，rows
    """
    ports_obj_all = Ports.objects.filter(host__name=asset_name)
    filter_str = request.GET.get('filter')
    ports_obj = ports_obj_all
    if filter_str:
        pass

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(ports_obj, request)
    total = ports_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        ports_filter = Ports.objects.get(id=r_dict['id'])
        r_dict['type'] = ports_filter.get_port_type_display()
        r_dict['ip'] = ports_filter.ip.ipaddress
        r_dict['description'] = '' if r_dict['description'] == None else r_dict['description']
        r_dict['port_type'] = '' if r_dict['port_type'] == None else r_dict['port_type']
        r_dict['create_person'] = User.objects.get(id=r_dict['create_person_id']).username
        r_dict['update_person'] = User.objects.get(id=r_dict['update_person_id']).username
        rows_list.append(r_dict)
    print rows_list
    return HttpResponse(json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder))

@require_role(role='user')
def asset_detail_ports_add(request,asset_type,asset_name):
    """
    添加端口
    """
    header_title, path1, path2 = u'添加端口', u'资产', u'详细信息'
    asset_name = asset_name
    asset_type = asset_type
    port_type_choice = Ports.PORT_TYPE_CHOICES
    port_connecte_choices = Ports.objects.all()
    ipaddress_choice = IPAddress.objects.filter(status='unuse')
    current_user = User.objects.get(username=request.user.username)  # 当前登录用户
    emg = ""  # error message
    smg = ""  # success message
    if request.method == "POST":
        print "request.POST:",request.POST
        postdata = copy.deepcopy(request.POST)
        # contract = [] if postdata.get('contract','') == '' else postdata.get('contract')
        host = models.Asset.objects.get(name=asset_name)
        postdata['host'] = host.id
        postdata['create_person'] = current_user.id
        postdata['update_person'] = current_user.id
        port_num = postdata["port_num"]
        ip_id = postdata['ip']
        port_ip_obj = IPAddress.objects.get(id=ip_id)
        port_filter = Ports.objects.filter(host=postdata['host'], port_num=port_num)
        if not port_filter.exists():
            port_form = PortsForm(postdata)
            if port_form.is_valid():
                # port_form_obj = port_form.save(commit=False)
                # port_form_obj.create_person = current_user
                # port_form_obj.update_person = current_user
                # port_form_obj.save()
                port_form.save()
                port_ip_obj.status = "inuse"
                port_ip_obj.save()
                port_ip_obj.segment.used_num = int(port_ip_obj.segment.used_num) + 1
                port_ip_obj.segment.unused_num = int(port_ip_obj.segment.unused_num) - 1
                port_ip_obj.segment.save()
                smg = u' %s添加成功' % port_num
            else:
                emg = port_form.errors.as_json()
        else:
            emg = u'添加失败, 此端口 %s 已存在!' % port_num
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iasset/asset/detail/ports/add.html', locals(), request)

@require_role(role='user')
def asset_detail_ports_edit(request,asset_type,asset_name):
    """
    编辑端口
    """
    header_title, path1, path2 = u'编辑端口', u'资产', u'详细信息'
    asset_name = asset_name
    asset_type = asset_type
    port_type_choice = Ports.PORT_TYPE_CHOICES
    port_connecte_choices = Ports.objects.all()
    ipaddress_choice = IPAddress.objects.filter(status='unuse')
    current_user = User.objects.get(username=request.user.username)  # 当前登录用户
    emg = ""  # error message
    smg = ""  # success message
    if request.method == "GET":
        port_id = request.GET["id"]
        try:
            port_obj = Ports.objects.get(id=port_id)
        except Exception,e:
            print "error:", e
            return HttpResponse(json.dumps({"emg": u"没有发现该端口"}))
        else:
            pass
    if request.method == "POST":
        print "request.POST:",request.POST
        postdata = copy.deepcopy(request.POST)
        host = models.Asset.objects.get(name=asset_name)
        postdata['host'] = host.id
        postdata['create_person'] = current_user.id
        postdata['update_person'] = current_user.id
        port_id = postdata['port_id']
        port_obj_old = Ports.objects.get(id=port_id)
        port_num_old = port_obj_old.port_num
        port_num_new = postdata["port_num"]
        port_ip_old = port_obj_old.ip
        port_ip_new = IPAddress.objects.get(id=postdata['ip'])
        port_obj_new = Ports.objects.filter(host=postdata['host'], port_num=port_num_new)
        if port_num_new!=port_num_old and port_obj_new.exists():
            emg = u'编辑失败, 此端口 %s 已存在!' % port_num_new
        else:
            port_form = PortsForm(postdata, instance=port_obj_old)
            if port_form.is_valid():
                # port_form_obj = port_form.save(commit=False)
                # port_form_obj.create_person = current_user
                # port_form_obj.update_person = current_user
                # port_form_obj.save()
                port_form.save()
                if port_ip_new.ipaddress != port_ip_old.ipaddress: #ip改变，ip使用数量也要改变
                    port_ip_old.segment.used_num = int(port_ip_old.segment.used_num) - 1
                    port_ip_old.segment.unused_num = int(port_ip_old.segment.unused_num) + 1
                    port_ip_old.segment.save()
                    port_ip_old.status = "unuse"
                    port_ip_old.save()
                    port_ip_new.status = "inuse"
                    port_ip_new.save()
                    port_ip_new.segment.used_num = int(port_ip_new.segment.used_num) + 1
                    port_ip_new.segment.unused_num = int(port_ip_new.segment.unused_num) - 1
                    port_ip_new.segment.save()
                smg = u' %s编辑成功' % port_num_new
            else:
                emg = port_form.errors.as_json()
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iasset/asset/detail/ports/edit.html', locals(), request)

@require_role(role='user')
def asset_detail_ports_delete(request,asset_type,asset_name):
    """
    删除端口
    如果端口上绑定了IP，需要将IP释放，并将网段中ip使用数量重新计数
    """
    smg = []  # success message
    emg = []  # error message
    if request.method == "POST":
        postdata = copy.deepcopy(request.POST)
        print "postdata:", postdata
        id_select = request.POST.getlist("id_select", [])
        print "ports_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    ports_select = Ports.objects.get(id=i)
                    ports_select.ip.status = 'unuse'
                    ports_select.ip.save()
                    ports_select.ip.segment.unused_num = int(ports_select.ip.segment.unused_num) + 1
                    ports_select.ip.segment.used_num = int(ports_select.ip.segment.used_num) - 1
                    ports_select.ip.segment.save()
                    ports_select.ip = None     #释放IP
                    ports_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s的%s端口删除成功" % (ports_select.ip.ipaddress, ports_select.port_num))
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))


@require_role(role='user')
def asset_detail_parts_list(request,asset_type,asset_name):
    """
    设备配件列表
    :param request:
    :param asset_type:  设备类型
    :param asset_name:  设备名称
    :return:            total，rows
    """
    parts_obj_all = models.Parts.objects.all()
    filter_str = request.GET.get('filter')
    parts_obj = parts_obj_all
    if filter_str:
        pass

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(parts_obj, request)
    total = parts_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        rows_list.append(r_dict)
    return HttpResponse(json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder))

@require_role(role='user')
def asset_detail_parts_add(request,asset_type,asset_name):
    pass

@require_role(role='user')
def asset_detail_parts_edit(request,asset_type,asset_name):
    pass
@require_role(role='user')
def asset_detail_parts_delete(request,asset_type,asset_name):
    pass

@require_role(role='user')
def asset_detail_contract_list(request,asset_type,asset_name):
    """
    设备合同信息
    :param request:
    :param asset_type:  设备类型
    :param asset_name:  设备名称
    :return:            total，rows
    """
    contract_obj_all = Contract.objects.all()
    filter_str = request.GET.get('filter')
    contract_obj = contract_obj_all
    if filter_str:
        pass

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(contract_obj, request)
    total = contract_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        rows_list.append(r_dict)
    return HttpResponse(json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder))

@require_role(role='user')
def asset_detail_contract_add(request,asset_type,asset_name):
    pass
@require_role(role='user')
def asset_detail_contract_edit(request,asset_type,asset_name):
    pass
@require_role(role='user')
def asset_detail_contract_delete(request,asset_type,asset_name):
    pass

@require_role(role='user')
def asset_detail_history_list(request,asset_type,asset_name):
    """
    设备端口列表
    :param request:
    :param asset_type:  设备类型
    :param asset_name:  设备名称
    :return:            total，rows
    """
    log_obj_all = EventLog.objects.all()
    filter_str = request.GET.get('filter')
    log_obj = log_obj_all
    if filter_str:
        pass

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(log_obj, request)
    total = log_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        rows_list.append(r_dict)
    return HttpResponse(json.dumps({'total': total,'rows': rows_list},cls=DatetimeEncoder))


# @require_role(role='user')
# def asset_edit(request):
#     header_title, path1, path2 = u'编辑', u'资产', u'编辑'
#     return my_render('iasset/asset/edit/index.html', locals(), request)
#
# @require_role(role='user')
# def asset_edit_batch(request):
#     header_title, path1, path2 = u'批量编辑', u'资产', u'批量编辑'
#     return my_render('iasset/asset/edit/batch.html', locals(), request)
@require_role(role='user')
def asset_update(request):
    header_title, path1, path2 = u'更新', u'资产', u'更新'
    return my_render('iasset/asset/update/index.html', locals(), request)
@require_role(role='user')
def asset_update_batch(request):
    header_title, path1, path2 = u'批量更新', u'资产', u'批量更新'
    return my_render('iasset/asset/update/batch.html', locals(), request)

@require_role(role='user')
def asset_manage(request):
    """
    基本信息管理
    """
    header_title, path1, path2 = u'管理', u'资产', u'管理'
    # return my_render('iasset/dashboard.html', locals(), request)
    return my_render('iasset/manage/idc/list.html', locals(), request)
@require_role(role='user')
def manage_idc(request):
    """
    机房管理
    """
    header_title, path1, path2, path3 = u'机房', u'资产', u'管理', u'机房'
    return my_render('iasset/manage/idc/list.html', locals(), request)
@require_role(role='user')
def manage_idc_list(request):
    """
    IDC列表
    """
    idc_obj_all = models.IDC.objects.all()
    filter_str = request.GET.get('filter')
    idc_obj = idc_obj_all
    #关键字过滤
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("name"):
            idc_obj = idc_obj.filter(name__icontains=filter_dict["name"].strip())
        if filter_dict.has_key("address"):
            idc_obj = idc_obj.filter(address__icontains=filter_dict["address"].strip())
        if filter_dict.has_key("status"):
            for k,v in dict(models.SIMPLE_STATUS_CHOICES).iteritems():
                if v.encode("utf-8") == filter_dict["status"]:
                    status_key = k
            idc_obj = idc_obj.filter(status=status_key)
        if filter_dict.has_key("memo"):
            idc_obj = idc_obj.filter(memo__icontains=filter_dict["memo"].strip())

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(idc_obj, request)
    total = idc_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        idc_select = models.IDC.objects.get(name=r_dict['name'])
        r_dict["status"] = idc_select.get_status_display()
        r_dict["isself"] = idc_select.get_isself_display()
        r_dict['cost'] = '' if r_dict['cost'] == None else r_dict['cost']
        r_dict['start_date'] = '' if r_dict['start_date'] == None else r_dict['start_date']
        r_dict['end_date'] = '' if r_dict['end_date'] == None else r_dict['end_date']
        rows_list.append(r_dict)
    print "rows_list:", rows_list
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='user')
def manage_idc_add(request):
    """
    添加IDC
    """
    header_title, path1, path2 = u'添加机房', u'资产', u'机房'
    isself_choices = models.SELF_OR_LEASE_CHOICES
    status_choices = models.SIMPLE_STATUS_CHOICES
    emg = ""  # error message
    smg = ""  # success message
    if request.method == "POST":
        print "request.POST:",request.POST
        postdata = copy.deepcopy(request.POST)
        # postdata = request.POST
        # contact = '' if postdata.get('contact','') == '' else postdata.get('contact')
        contract = [] if postdata.get('contract','') == '' else postdata.get('contract')
        # print "contact contract：", contact,contract
        # postdata['contract'] = [] if postdata['contract'] =='' or postdata['contract'] == None else postdata['contract']
        idc_form = IdcForm(postdata)
        # print "idc_form:",idc_form
        if idc_form.is_valid():
            idc_name = idc_form.cleaned_data['name']
            print "idc_name:",idc_name
            if models.IDC.objects.filter(name=idc_name):
                emg = u'添加失败, 此IDC %s 已存在!' % idc_name
            else:
                idc_obj = idc_form.save(commit=False)
                try: #由于idc和contract之间是多对多关系，默认不能为空，所以要单拿出来添加，如果提交的数据中contract为空，那么不添加该字段到数据库。
                    contract_obj = Contract.objects.get(id=postdata['contract'])
                except Exception,e:
                    print e
                else:
                    idc_obj.contract.add(contract_obj)
                idc_obj.save()
                smg = u'IDC: %s添加成功' % idc_name
        else:
            emg = idc_form.errors.as_json()
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iasset/manage/idc/add.html', locals(), request)
@require_role(role='super')
def manage_idc_delete(request):
    """
    删除IDC
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
                    idc_select = models.IDC.objects.get(id=i)
                    idc_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功\n" % idc_select.name)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
@require_role(role='user')
def manage_idc_edit(request):
    """
    编辑IDC
    """
    header_title, path1, path2 = u'编辑机房', u'资产', u'机房'
    isself_choices = models.SELF_OR_LEASE_CHOICES
    status_choices = models.SIMPLE_STATUS_CHOICES
    emg = ""  # error message
    smg = ""  # success message
    if request.method == 'GET':
        idc_name = request.GET["name"]
        try:
            idc_detail = models.IDC.objects.get(name=idc_name)
        except Exception,e:
            emg = u'更新失败, 此IDC %s 不存在!' % idc_name
        return my_render('iasset/manage/idc/edit.html', locals(), request)
    if request.method == "POST":
        post_data = request.POST
        idc_obj = models.IDC.objects.get(name=post_data.get("name"))
        idc_form = IdcForm(post_data,instance=idc_obj)
        if idc_form.is_valid():
            idc_form.save()
            smg = u'IDC: %s更新成功' % idc_name
        else:
            emg = u'更新失败',idc_form.non_field_errors()
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='user')
def manage_os(request):
    """
    操作系统管理
    """
    header_title, path1, path2 = u'操作系统列表', u'资产', u'操作系统'
    os_list = models.OS.objects.all()
    return my_render('iasset/manage/os/list.html', locals(), request)
@require_role(role='user')
def manage_os_list(request):
    """
    操作系统版本列表
    :param request:
    :return:
    """
    os_obj_all = models.OS.objects.all()
    filter_str = request.GET.get('filter')
    os_obj = os_obj_all
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("version"):
            os_obj = os_obj.filter(version__icontains=filter_dict["version"].strip())
        if filter_dict.has_key("os_type"):
            for k,v in dict(models.OS_TYPE_CHOICES).iteritems():
                if v.encode("utf-8") == filter_dict["os_type"]:
                    os_type_key = k
            os_obj = os_obj.filter(os_type__icontains=os_type_key)
        if filter_dict.has_key("soft_license"):
            os_obj = os_obj.filter(soft_license__icontains=filter_dict["soft_license"].strip())
        if filter_dict.has_key("memo"):
            os_obj = os_obj.filter(memo__icontains=filter_dict["memo"].strip())

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(os_obj, request)
    total = os_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        os_filter = models.OS.objects.get(version=r_dict["version"])
        r_dict["os_type"] = os_filter.get_os_type_display()
        rows_list.append(r_dict)
    print "rows_list:",rows_list
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='user')
def manage_os_delete(request):
    """
    删除操作系统类型
    """
    smg = []  # success message
    emg = []  # error message
    print u"开始删除操作系统类型..."
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    os_select = models.OS.objects.get(id=i)
                    os_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功" % os_select.version)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
@require_role(role='user')
def manage_os_edit(request):
    """
     os编辑界面
    """
    header_title, path1, path2 = u'编辑操作系统类型', u'资产', u'管理'
    ostype_select = models.OS_TYPE_CHOICES
    smg = '' #success message
    emg = '' #error message
    if request.method == "GET":
        os_version = request.GET["version"]
        try:
            os_detail = models.OS.objects.get(version=os_version)
        except Exception, e:
            emg = u"该操作系统类型不存在"
        return my_render('iasset/manage/os/edit.html', locals(), request)
    if request.method == "POST":
        version = request.POST.get("version")
        ostype = request.POST.get("ostype")
        license = request.POST.get("license","")
        memo = request.POST.get("memo","")
        try:
            os_filter = models.OS.objects.filter(version=version)
        except Exception, e:
            emg = e
        else:
            try:
                os_filter.update(version=version,os_type=ostype,soft_license=license,memo=memo,update_date=datetime.now(tz=""))
            except Exception, e:
                emg = u"错误:",e
            else:
                smg = u"更新成功！"
        return HttpResponse(json.dumps({"smg":smg,"emg":emg}))
@require_role(role='user')
def manage_os_add(request):
    """
    操作系统添加
    :param request:
    :return:
    """
    header_title, path1, path2 = u'添加操作系统', u'资产', u'操作系统'
    ostype_select = models.OS_TYPE_CHOICES
    emg = ""  #error message
    smg = ""  #success message
    if request.method == "GET":
        return my_render('iasset/manage/os/add.html', locals(), request)

    if request.method == "POST":
        print request.POST
        ostype = request.POST.get("ostype")
        version = request.POST.get("version").strip()
        license = request.POST.get("license","")
        memo = request.POST.get("memo","")
        try:
            if models.OS.objects.filter(version=unicode(version)):
                emg = u"添加失败，该版本 %s 已存在" % version
                raise ServerError(emg)
        except ServerError:
            pass
        else:
            models.OS.objects.create(os_type=ostype, version=version, soft_license=license, memo=memo)
            smg = u"%s 添加成功" % version
        return HttpResponse(json.dumps({"smg":smg,"emg":emg}))


# def manage_os_detail(request):
#     """
#     操作系统详细
#     :param request:
#     :return:
#     """
#
#     return my_render('iasset/manage/os/detail.html', locals(), request)
# @require_role(role='user')
# def manage_tag(request):
#     """
#     标签管理
#     """
#     header_title, path1, path2, path3 = u'标签管理', u'资产', u'管理', u'标签'
#     return my_render('iasset/manage/tag/list.html', locals(), request)

@require_role(role='user')
def manage_cabinet(request):
    """机柜列表"""
    header_title, path1, path2 = u'机柜列表', u'资产', u'机柜'
    # cabinet_all = models.Cabinet.objects.all()
    return my_render('iasset/manage/cabinet/list.html', locals(), request)
@require_role(role='user')
def manage_cabinet_list(request):
    """机柜列表"""
    filter_str = request.GET.get('filter')
    cabinet_obj_all = models.Cabinet.objects.all()
    cabinet_obj = cabinet_obj_all
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key('name'):
            cabinet_obj = cabinet_obj.filter(name__regex=filter_dict['name'])
        if filter_dict.has_key('idc'):
            cabinet_obj = cabinet_obj.filter(idc__name__regex=filter_dict['idc'])
        if filter_dict.has_key('location'):
            cabinet_obj = cabinet_obj.filter(location__regex=filter_dict['location'])
        if filter_dict.has_key('layer'):
            cabinet_obj = cabinet_obj.filter(layer__regex=filter_dict['layer'])
        if filter_dict.has_key('status'):
            for k,v in dict(models.SIMPLE_STATUS_CHOICES).iteritems():
                if v.encode("utf-8") == filter_dict["status"]:
                    status_key = k
            cabinet_obj = cabinet_obj.filter(status=status_key)
        if filter_dict.has_key('memo'):
            cabinet_obj = cabinet_obj.filter(memo__regex=filter_dict['memo'])


    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(cabinet_obj, request)
    total = cabinet_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        # os_filter = models.OS.objects.get(version=r_dict["version"])
        cabinet_filter = models.Cabinet.objects.get(name=r_dict['name'])
        r_dict['status'] = cabinet_filter.get_status_display()
        r_dict['idc'] = '' if r_dict["idc_id"]==None or r_dict["idc_id"]=='' else models.IDC.objects.get(id=r_dict["idc_id"]).name
        # r_dict["os_type"] = os_filter.get_os_type_display()
        rows_list.append(r_dict)
    print "rows_list:", rows_list
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='user')
def manage_cabinet_add(request):
    """机柜添加"""
    header_title, path1, path2 = u'添加机柜', u'资产', u'机柜'
    smg = ''   #success message
    emg = ''   #error   message
    status_choices = models.SIMPLE_STATUS_CHOICES
    idc_all = models.IDC.objects.all()
    if request.method == "POST":
        cabinet_form = CabinetForm(request.POST)
        cabinet_name = request.POST.get('name')
        if models.Cabinet.objects.filter(name=cabinet_name).exists():
            emg = u"%s 已存在" % cabinet_name
        else:
            if cabinet_form.is_valid():
                cabinet_form.save()
                smg = u"%s 添加成功" % cabinet_name
            else:
                emg = cabinet_form.errors.as_json()
                print "emg:",emg
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('iasset/manage/cabinet/add.html', locals(), request)
@require_role(role='super')
def manage_cabinet_delete(request):
    """机柜删除"""
    smg = []  # success message
    emg = []  # error message
    print u"开始删除机柜..."
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "cabinet_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    cabinet_select = models.Cabinet.objects.get(id=i)
                    cabinet_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    smg.append(u"%s 删除成功\n" % cabinet_select.name)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='user')
def manage_cabinet_edit(request):
    """机柜编辑"""
    header_title, path1, path2 = u'编辑机柜', u'资产', u'机柜'
    smg = ''  # success message
    emg = ''  # error message
    status_choices = models.SIMPLE_STATUS_CHOICES
    idc_all = models.IDC.objects.all()
    if request.method == 'GET':
        cabinet_name = request.GET["name"]
        try:
            cabinet_detail = models.Cabinet.objects.get(name=cabinet_name)
        except Exception, e:
            emg = u"该机柜不存在"
        return my_render('iasset/manage/cabinet/edit.html', locals(), request)
    if request.method == 'POST':
        post_data = request.POST
        cabinet_obj = models.Cabinet.objects.get(name=post_data.get("name"))
        update_form = CabinetForm(post_data,instance=cabinet_obj)
        if update_form.is_valid():
            update_form.save()
            smg = u"%s 更新成功" % cabinet_obj.name
        else:
            emg = update_form.non_field_errors()
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))