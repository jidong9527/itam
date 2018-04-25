#_*_coding:utf-8_*_
__author__ = 'jidong'
from django.shortcuts import render,render_to_response

# Create your views here.
from itam.api import *
from inetwork import models
from iservice.models import ServiceInfo
from iuser.models import User

@require_role(role='user')
def network_ip(request):
    header_title, path1, path2 = u'IP列表', u'网络', u'IP'
    return my_render('inetwork/ip/list.html', locals(), request)
@require_role(role='user')
def network_ip_list(request):
    """
    IP信息列表
    """
    ip_obj_all = models.IPAddress.objects.all()
    ip_obj = ip_obj_all
    filter_str = request.GET.get('filter')
    # 关键字过滤
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("ipaddress"):
            ip_obj = ip_obj.filter(ipaddress__contains=filter_dict["ipaddress"].strip())
        if filter_dict.has_key("status"):
            key = choice_code(models.STATUS_CHOICES, filter_dict["status"])
            ip_obj = ip_obj.filter(status=key)
        if filter_dict.has_key("memo"):
            ip_obj = ip_obj.filter(memo__icontains=filter_dict["memo"])
    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(ip_obj, request)
    total = ip_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        segment_filter = models.Segment.objects.get(id=r_dict["segment_id"])
        ip_filter = models.IPAddress.objects.get(id=r_dict["id"])
        r_dict["device"] = '' if r_dict["status"]=="unuse" else ip_filter.ports_set.all().first().host.name
        r_dict["asset_type_key"] = '' if r_dict["device"] == '' else ip_filter.ports_set.all().first().host.model.asset_type
        r_dict["segment"] = str(IP(segment_filter.address).make_net(segment_filter.mask))
        r_dict["status"] = ip_filter.get_status_display()
        r_dict["service"] = '' if r_dict["service_id"]== None else ServiceInfo.objects.get(id=r_dict["service_id"]).name
        r_dict['create_person'] = User.objects.get(id=r_dict['create_person_id']).username
        r_dict['update_person'] = User.objects.get(id=r_dict['update_person_id']).username
        rows_list.append(r_dict)
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='user')
def network_ip_add(request):
    header_title, path1, path2 = u'添加IP', u'网络', u'IP'
    status_choices = models.STATUS_CHOICES
    segment_choices = models.Segment.objects.all()
    service_choices = ServiceInfo.objects.all()
    smg = []
    emg = []
    if request.method == "POST":
        current_user = User.objects.get(username=request.user.username)
        postdict = request.POST
        status = postdict['status']
        service_id = postdict['service']
        ipaddress = postdict['ipaddress']
        memo = postdict['memo']
        user = postdict['user']
        segment_id = postdict['segment']
        # port_id = None
        create_person = current_user
        update_person = current_user
        segment_filter = models.Segment.objects.get(id=segment_id)
        service_filter = None if service_id=='' else models.ServiceInfo.objects.get(id=service_id)
        if valid_ip(ipaddress):
            net = IP(segment_filter.address).make_net(segment_filter.mask)
            if ipaddress in net:
                if models.IPAddress.objects.filter(ipaddress=ipaddress).exists():
                    emg = u"IP：%s 已存在" % ipaddress
                else:
                    ipaddress_obj = models.IPAddress(ipaddress=ipaddress,segment=segment_filter,
                                     status=status,user=user,service=service_filter,
                                     create_person=create_person,
                                     update_person=update_person,memo=memo)
                    ipaddress_obj.save()
                    segment_filter.used_num = models.IPAddress.objects.filter(status="inuse",segment_id=segment_id).count()
                    segment_filter.unused_num = models.IPAddress.objects.filter(status="unuse",segment_id=segment_id).count()
                    segment_filter.save()
                    smg = u"%s添加成功" % ipaddress
            else:
                emg = u"添加失败，%s 不在网段 %s里" % (ipaddress,net)
        else:
            emg = u"IP：%s 格式不正确" % ipaddress

        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('inetwork/ip/add.html', locals(), request)
@require_role(role='user')
def network_ip_edit(request):
    header_title, path1, path2 = u'编辑IP', u'网络', u'IP'
    status_choices = models.STATUS_CHOICES
    segment_choices = models.Segment.objects.all()
    service_choices = ServiceInfo.objects.all()
    smg = []
    emg = []
    if request.method == "GET":
        ip = request.GET["ip"]
        try:
            ip_detail = models.IPAddress.objects.get(ipaddress=ip)
        except Exception,e:
            emg = u'更新失败, 此IP %s 不存在!' % ip
        return my_render('inetwork/ip/edit.html', locals(), request)
    if request.method == "POST":
        current_user = User.objects.get(username=request.user.username)
        postdict = request.POST
        print postdict
        status = postdict['status']
        service_id = postdict['service']
        ipaddress = postdict['ipaddress']
        memo = postdict['memo']
        user = postdict['user']
        ip_detail = models.IPAddress.objects.get(ipaddress=ipaddress)
        segment_id = ip_detail.segment_id
        # port_id = None
        # create_person = current_user
        update_person = current_user
        segment_filter = models.Segment.objects.get(id=segment_id)
        service_filter = None if service_id=='' else models.ServiceInfo.objects.get(id=service_id)
        if valid_ip(ipaddress):
            net = IP(segment_filter.address).make_net(segment_filter.mask)
            if ipaddress in net:
                # ipaddress_obj = models.IPAddress(ipaddress=ipaddress,segment=segment_filter,
                #                  status=status,user=user,service=service_filter,
                #                  port=port_id,create_person=create_person,
                #                  update_person=update_person,memo=memo)
                ipaddress_obj = models.IPAddress.objects.get(ipaddress=ipaddress)
                ipaddress_obj.status = status
                ipaddress_obj.user = user
                ipaddress_obj.service_id = service_id
                ipaddress_obj.update_person = update_person
                ipaddress_obj.memo = memo
                ipaddress_obj.save()
                segment_filter.used_num = models.IPAddress.objects.filter(status="inuse",segment_id=segment_id).count()
                segment_filter.unused_num = models.IPAddress.objects.filter(status="unuse",segment_id=segment_id).count()
                segment_filter.save()
                smg = u"%s修改成功" % ipaddress
            else:
                emg = u"修改失败，%s 不在网段 %s里" % (ipaddress,net)
        else:
            emg = u"修改失败，IP：%s 格式不正确" % ipaddress

        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='super')
def network_ip_delete(request):
    """
    删除IP
    """
    smg = []  # success message
    emg = []  # error message
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "idc_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                try:
                    ip_select = models.IPAddress.objects.get(id=i)
                    ip_select.delete()
                except Exception, e:
                    emg.append(e)
                else:
                    segment_filter = ip_select.segment
                    segment_filter.used_num = models.IPAddress.objects.filter(status="inuse",segment_id=ip_select.segment_id).count()
                    segment_filter.unused_num = models.IPAddress.objects.filter(status="unuse",segment_id=ip_select.segment_id).count()
                    segment_filter.save()
                    smg.append(u"%s 删除成功\n" % ip_select.ipaddress)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='user')
def network_segment(request):
    header_title, path1, path2 = u'网段', u'网络', u'网段'
    return my_render('inetwork/segment/list.html', locals(), request)
@require_role(role='user')
def network_segment_list(request):
    """
    网段信息列表
    """
    segment_obj_all = models.Segment.objects.all()
    segment_obj = segment_obj_all
    filter_str = request.GET.get('filter')
    # 关键字过滤
    if filter_str:
        filter_dict = eval(filter_str)
        if filter_dict.has_key("address"):
            segment_obj = segment_obj.filter(address__exact=filter_dict["address"])
        if filter_dict.has_key("usage"):
            segment_obj = segment_obj.filter(usage__icontains=filter_dict["usage"])
        if filter_dict.has_key("used_num"):
            segment_obj = segment_obj.filter(used_num=filter_dict["used_num"])
        if filter_dict.has_key("unused_num"):
            segment_obj = segment_obj.filter(unused_num=filter_dict["unused_num"])
        if filter_dict.has_key("memo"):
            segment_obj = segment_obj.filter(memo__icontains=filter_dict["memo"])
    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    contacts_all, paginator, rows, page_range, current_page, show_first, show_end = pages(segment_obj, request)
    total = segment_obj.count()
    rows_list = []
    for r in rows.object_list:
        r_dict = class_to_dict(r)
        r_dict['create_person'] = User.objects.get(id=r_dict['create_person_id']).username
        r_dict['update_person'] = User.objects.get(id=r_dict['update_person_id']).username
        rows_list.append(r_dict)
    return HttpResponse(json.dumps({'total': total, 'rows': rows_list}, cls=DatetimeEncoder))
@require_role(role='user')
def network_segment_add(request):
    header_title, path1, path2 = u'添加网段', u'网络', u'网段'
    version_choices = models.IP_TYPE_CHOICES
    smg = []
    emg = []
    if request.method == "POST":
        print request.POST
        address = request.POST.get('address')
        mask = request.POST.get('mask')
        ip_version = request.POST.get('ip_version')
        generateip = request.POST.get('generateip')  #yes:需自动生成IP，no:不需要生成IP
        usage = request.POST.get('usage','')
        memo = request.POST.get('memo','')
        ip_mask = '%s/%s' % (address,mask)
        print "ip_mask:",ip_mask
        current_user = User.objects.get(username=request.user.username)
        if valid_ip(ip_mask):
            ips = IP(ip_mask)
            print "ips.version():",ips.version()
            if not models.Segment.objects.filter(address=address,mask=mask):
                segment_obj = models.Segment(ip_version=ip_version,address=address,mask=mask,
                                         usage=usage,used_num="0",unused_num=str(ips.len()),
                                         create_person=current_user,update_person=current_user,
                                         memo=memo)
                success_num,error_num = 0,0
                try:
                    segment_obj.save()
                except Exception,e:
                    print "save error:",e
                    emg = u'添加失败，%s' % e
                else:
                    if generateip == 'yes':
                        segment_filter = models.Segment.objects.get(id=segment_obj.id)
                        for ip in ips:
                            print "ip:",ip
                            ipfilter = models.IPAddress.objects.filter(ipaddress=str(ip))
                            print "ipfilter:",ipfilter
                            if ipfilter:
                                emg.append(u'%s 已存在' % ip)
                                print "emg:",emg
                                error_num += 1
                            else:
                                try:
                                    ipaddress_obj = models.IPAddress(ipaddress=str(ip),
                                                                     segment=segment_filter,
                                                                     status='unuse',
                                                                     service=None,
                                                                     user='',
                                                                     memo='',
                                                                     create_person=current_user,
                                                                     update_person=current_user)

                                    # print "ipaddress_obj:"
                                except Exception,e:
                                    print "error:",e
                                else:
                                    print "ipaddress_obj.save()..."
                                    ipaddress_obj.save()
                                    success_num += 1
                                    print 'success_num:',success_num
                        smg = u'网段 %s 添加成功，%d个ip创建成功，%d个ip创建失败\n %s' % (ip_mask,success_num,error_num,emg)
                    else:
                        smg = u'网段 %s 添加成功,没有IP被创建' % ip_mask
            else:
                emg = u'添加失败，%s 网段已存在' % ip_mask
        else:
            emg = u"添加失败,网段地址或者掩码长度不正确"
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))
    return my_render('inetwork/segment/add.html', locals(), request)
@require_role(role='user')
def network_segment_edit(request):
    header_title, path1, path2 = u'编辑网段', u'网络', u'网段'
    version_choices = models.IP_TYPE_CHOICES
    version_choices = models.IP_TYPE_CHOICES
    smg = []
    emg = []
    if request.method == "GET":
        try:
            id = request.GET["id"]
            segment_detail = models.Segment.objects.get(id=id)
        except Exception,e:
            emg = u'更新失败, 此网段id %s 不存在!' % id
        return my_render('inetwork/segment/edit.html', locals(), request)
    if request.method == "POST":
        print request.POST
        address = request.POST.get('address')
        mask = request.POST.get('mask')
        ip_version = request.POST.get('ip_version')
        generateip = request.POST.get('generateip')  #yes:需自动生成IP，no:不需要生成IP
        usage = request.POST.get('usage','')
        memo = request.POST.get('memo','')
        ip_mask = '%s/%s' % (address,mask)
        print "ip_mask:",ip_mask
        current_user = User.objects.get(username=request.user.username)
        if valid_ip(ip_mask):
            ips = IP(ip_mask)
            print "ips.version():", ips.version()
            if models.Segment.objects.filter(address=address, mask=mask).exists():
                # segment_obj = models.Segment(ip_version=ip_version,address=address,mask=mask,
                #                          usage=usage,used_num="0",unused_num=str(ips.len()),
                #                          create_person=current_user,update_person=current_user,
                #                          memo=memo)
                success_num, error_num = 0, 0
                try:
                    segment_obj = models.Segment.objects.get(address=address, mask=mask)
                    segment_obj.usage = usage
                    segment_obj.update_person = current_user
                    segment_obj.memo = memo
                    segment_obj.save()
                except Exception, e:
                    print u"save error:", e
                    emg = u'更新失败，%s' % e
                else:
                    if generateip == 'yes':
                        # segment_filter = models.Segment.objects.get(id=segment_obj.id)
                        for ip in ips:
                            print "generating ip:", ip
                            ipfilter = models.IPAddress.objects.filter(ipaddress=str(ip))
                            # print "ipfilter:", ipfilter
                            if ipfilter:
                                emg.append(u'%s 已存在' % ip)
                                print "emg:", emg
                                error_num += 1
                            else:
                                try:
                                    ipaddress_obj = models.IPAddress(ipaddress=str(ip),
                                                                     segment=segment_obj,
                                                                     status='unuse',
                                                                     service=None,
                                                                     user='',
                                                                     memo='',
                                                                     create_person=current_user,
                                                                     update_person=current_user)

                                    # print "ipaddress_obj:"
                                except Exception, e:
                                    print "error:", e
                                else:
                                    print "ipaddress_obj.save()..."
                                    ipaddress_obj.save()
                                    success_num += 1
                                    print 'success_num:', success_num
                        error = u''
                        for e in emg:
                            error = error + e + "; "
                        smg = u'网段 %s 更新成功，%d个ip创建成功，%d个ip创建失败。\n %s' % (ip_mask, success_num, error_num, error)
                    else:
                        smg = u'网段 %s 更新成功,没有IP被创建' % ip_mask

            else:
                emg = u'更新失败，%s 网段不存在' % ip_mask
        else:
            emg = u"编辑失败,网段地址格式不正确"
        return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='super')
def network_segment_delete(request):
    """
    删除网段，先判断该网段下是否存在IP，若存在，再判断这些IP是否都被占用，占用则不能删除，除非手动将被占用的IP解除。
    若该网段下不存在IP或者IP都为被占用，则直接删除该网段及下面所有IP。
    """
    smg = ''  # success message
    emg = ''  # error message
    if request.method == "POST":
        # post_data = request.POST
        id_select = request.POST.getlist("id_select", [])
        print "idc_id_select:", id_select, type(id_select)
        if id_select:
            for i in id_select:
                seg_select = models.Segment.objects.get(id=i)
                seg = "%s/%s" % (seg_select.address,seg_select.mask)
                ipaddress_set = seg_select.ipaddress_set
                if ipaddress_set.exists():    #如果网段下面有IP，那么就判断IP是否被占用
                    if ipaddress_set.all().filter(status="inuse").exists():
                        inuse_num = ipaddress_set.all().filter(status="inuse").count()
                        for ip in ipaddress_set.all():
                            inuse = ''
                            if ip.status == "inuse":
                                inuse += str(ip.ipaddress) + ";"
                        emg += u"由于%s网段下有%d个IP被占用，无法删除。请手动解除占用，再来删除该网段。下面是被占用的IP：%s \n" % (seg, inuse_num,inuse)
                    else:
                        # seg_select.delete()
                        smg += u"%s网段下有%d个IP，都未被占用,已经被删除\n" % (seg, ipaddress_set.all().count())
                else: #如果该网段下面没有IP，则可以删除。

                    # seg_select.delete()
                    smg += u"%s/%s 删除成功;\n" % (seg_select.address, seg_select.mask)
    return HttpResponse(json.dumps({"smg": smg, "emg": emg}))

@require_role(role='user')
def network_link(request):
    header_title, path1, path2 = u'链路', u'网络', u'链路'
    link_type = models.LINK_TYPE_CHOICES
    return my_render('inetwork/link/list.html', locals(), request)
@require_role(role='user')
def network_link_list(request):
    pass
@require_role(role='user')
def network_link_add(request):
    header_title, path1, path2 = u'添加链路', u'网络', u'链路'
    link_type = models.LINK_TYPE_CHOICES
    print request.POST
    return my_render('inetwork/link/add.html', locals(), request)
@require_role(role='user')
def network_link_edit(request):
    header_title, path1, path2 = u'编辑链路', u'网络', u'链路'
    link_type = models.LINK_TYPE_CHOICES
    return my_render('inetwork/link/edit.html', locals(), request)
@require_role(role='user')
def network_link_delete(request):
    pass
@require_role(role='user')
def network_topology(request):
    header_title, path1, path2 = u'拓扑图', u'网络', u'拓扑图'
    return my_render('inetwork/network_topology.html', locals(), request)