from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from pytz import timezone

import json
import datetime

from plugins.pager import Pagination
from EasyPermission.easyPermission import EasyPermission
from EasyPermission import settings_doc
from EasyPermission.models import Role, Role2User
from .models import Customer, User, Tis
from . import forms

# Create your views here.

ep = EasyPermission(settings_doc)
tz = timezone(settings.TIME_ZONE)  # 设置时区，和settings保持一致


def index(request):
    # 筛选近一周的用户
    now_time = datetime.datetime.now(tz)
    # 一周前
    last_time = now_time - datetime.timedelta(days=7)

    c_obj = Customer.objects.filter(create_time__lte=now_time, create_time__gte=last_time).all()

    payment_dic = {}
    non_payment_dic = {}
    i = 0
    for c in c_obj:

        if c.money:

            fmt_t = datetime.datetime.strftime(c.play_time, "%m-%d")
            payment_dic[fmt_t] = payment_dic.get(fmt_t, 0) + 1
        else:

            fmt_t = datetime.datetime.strftime(c.create_time, "%m-%d")

            non_payment_dic[fmt_t] = non_payment_dic.get(fmt_t, 0) + 1

    # 构造数据
    date_set = set(payment_dic) | set(non_payment_dic)
    date_data = sorted(date_set, key=lambda x: x)

    data = [{
        "name": '已付费',
        "type": 'line',
        "data": []
    },
        {
            "name": '未付费',
            "type": 'line',
            "data": []
        }]
    for d in date_data:
        payment_num = payment_dic.get(d, 0)
        non_payment_num = non_payment_dic.get(d, 0)
        data[0]["data"].append(payment_num)
        data[1]["data"].append(non_payment_num)
    return render(request, "index.html",
                  {"request": request, "now_page": "index", "data": str(data), "date_data": str(date_data)})


def gen_pwd(pwd):
    "对密码进行二次MD5加密"
    pwd = pwd.encode("utf8")
    import hashlib
    m = hashlib.md5()
    m.update(pwd)
    m.update(pwd)  # 加盐
    return m.hexdigest()


def logout(request):
    """退出登录，删除session中的数据"""
    if request.session.get("user_data"):
        del request.session["user_data"]
    if request.session.get("permission_list"):
        del request.session["permission_list"]
    return redirect("/")


def login(request):
    """登录，假如成功了，就把权限信息，和基本的用户信息放入到session中"""
    next_url = request.GET.get("next", "/")
    if request.method == "GET":
        if request.session.get("user_id"):
            return HttpResponse("已经登录")
        return render(request, "login.html", {"next_url": next_url})
    elif request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        msg = "密码为空"
        if password:
            password = gen_pwd(password)
            user = User.objects.filter(email=email, password=password).first()
            if user:
                # 写入信息
                user_id = user.id
                user_data = {
                    "username": user.username,
                    "user_id": user_id,
                }
                role = Role.objects.filter(role2user__user_id=user.id).first()
                if role:
                    user_data["role"] = settings.ROLE.get(role.id, "unknown")
                request.session["user_data"] = user_data
                request.session["permission_list"] = json.dumps(ep.gen_permission_list(user_id, serial=True))
                return redirect(next_url)
            msg = "账户或密码错误"
        return render(request, "login.html", {"next_url": next_url, "msg": msg, "request": request})


def customer_list(request):
    """获得客户列表"""
    c_obj = Customer.objects.all()
    page = request.GET.get("_page", 1)
    p = Pagination(c_obj.count(), page)
    c_obj = c_obj[p.start: p.end]
    page_li = p.page_str(reverse("web:customer_list"))
    return render(request, "customer.html",
                  {"request": request, "now_page": "customer_list", "c_obj": c_obj, "page_li": page_li})


def payment_list(request):
    """获得账单列表"""
    c_model = Customer.objects.all()
    page = request.GET.get("_page", 1)
    p = Pagination(c_model.count(), page)
    c_model = c_model[p.start: p.end]
    page_li = p.page_str(reverse("web:payment_list"))
    return render(request, "payment.html",
                  {"request": request, "now_page": "payment_list", "c_model": c_model, "page_li": page_li})


def payment_add(request):
    """使用ajax创建用户"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    data = {
        "username": request.POST.get("username"),
        "addr": request.POST.get("addr"),
        "phone_number": request.POST.get("phone_number")
    }
    try:
        money = int(request.POST.get("money"))
    except ValueError:
        res["status"] = 400
        res["msg"] = "请确缴费金额为数字"
        return HttpResponse(json.dumps(res), content_type="application/json")
    data["money"] = money
    form = forms.CustomerForm(data)

    if form.is_valid():
        data = dict(form.cleaned_data)
        data["play_time"] = datetime.datetime.now(tz)
        data["create_time"] = datetime.datetime.now(tz)

        c_obj = Customer.objects.create(**data)
        tips_data = {
            "operator_id": request.session.get("user_data").get("user_id"),
            "customer_id": c_obj.id,
            "action": "创建用户",
            "level": 1,
            "operator_time": datetime.datetime.now(tz)
        }
        Tis.objects.create(**tips_data)
        return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = "400"
    res["msg"] = "数据异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def payment_edit(request):
    """使用ajax修改账单"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    data = {
        "username": request.POST.get("username"),
        "addr": request.POST.get("addr"),
        "phone_number": request.POST.get("phone_number")}
    uid = request.POST.get("uid")
    if not uid:
        res["status"] = 400
        res["msg"] = "uid缺失"
        return HttpResponse(json.dumps(res), content_type="application/json")
    try:
        money = int(request.POST.get("money"))
    except ValueError:
        res["status"] = 400
        res["msg"] = "请确缴费金额为数字"
        return HttpResponse(json.dumps(res), content_type="application/json")
    data["money"] = money
    form = forms.CustomerForm(data)

    if form.is_valid():
        data = form.cleaned_data.copy()

        c_obj = Customer.objects.filter(pk=uid).first()
        if c_obj:
            tips_data = {
                "operator_id": request.session.get("user_data").get("user_id"),
                "customer_id": c_obj.id,
                "action": "修改用户信息",
                "level": 1,
                "operator_time": datetime.datetime.now(tz)
            }
            if c_obj.money == 0 and data.get("money"):
                data["play_time"] = datetime.datetime.now(tz)
                tips_data["action"] += "，缴费"
                tips_data["level"] = 2
            elif c_obj.money != 0 and data.get("money"):
                tips_data["action"] += "，修改缴费金额"
                tips_data["level"] = 2
            Customer.objects.filter(pk=uid).update(**data)
            Tis.objects.create(**tips_data)
            return HttpResponse(json.dumps(res), content_type="application/json")

    res["status"] = "400"
    res["msg"] = "数据异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def payment_del(request):
    """删除账单，会连带把用户一起删除"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    uid = request.POST.get("uid")
    c_obj = Customer.objects.filter(pk=uid).first()
    if c_obj:
        tips_data = {
            "operator_id": request.session.get("user_data").get("user_id"),
            "customer": None,
            "action": "删除用户 %s" % c_obj.username,
            "level": 3,
            "operator_time": datetime.datetime.now(tz)
        }
        Customer.objects.filter(pk=uid).delete()

        Tis.objects.create(**tips_data)
        return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = 400
    res["msg"] = "用户信息异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def staff_list(request):
    """获得员工列表"""
    u_model = User.objects.all()
    page = request.GET.get("_page", 1)
    p = Pagination(u_model.count(), page)
    u_model = u_model[p.start: p.end]
    page_li = p.page_str(reverse("web:staff_list"))
    return render(request, "staff.html",
                  {"request": request, "now_page": "staff_list", "u_model": u_model, "page_li": page_li})


def staff_add(request):
    """用ajax发送请求，添加员工信息"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    data = {
        "email": request.POST.get("email"),
        "username": request.POST.get("username"),
        "password": request.POST.get("password"),
        "note": request.POST.get("note", ""),

    }

    form = forms.UserForm(data)
    if form.is_valid():
        teacher_id = None
        finance_id = None
        role = request.POST.get("role")
        for k, v in settings.ROLE.items():
            if v == "teacher":
                teacher_id = k
            elif v == "finance":
                finance_id = k
        try:
            role = int(role)
            if role == 1:
                # teacher
                role = teacher_id
            elif role == 2:
                # finance
                role = finance_id
            else:
                res["status"] = "400"
                res["msg"] = "指定职务异常"
                return HttpResponse(json.dumps(res), content_type="application/json")
        except ValueError:
            res["status"] = "400"
            res["msg"] = "指定职务异常"
            return HttpResponse(json.dumps(res), content_type="application/json")

        import datetime
        data["entry_time"] = datetime.datetime.now(tz)
        data["password"] = gen_pwd(data["password"])
        u_obj = User.objects.create(**data)
        Role2User.objects.create(user_id=u_obj.pk, role_id=role)
        return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = "400"
    res["msg"] = "数据异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def staff_edit(request):
    """修改员工数据"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    uid = request.POST.get("uid")
    if not uid:
        res["status"] = 400
        res["msg"] = "uid缺失"
        return HttpResponse(json.dumps(res), content_type="application/json")
    form = forms.UserChangeForm(request.POST)

    if form.is_valid():
        c_obj = User.objects.filter(pk=uid).first()
        if c_obj:
            if request.POST.get("note"):
                note = request.POST.get("note")
                User.objects.filter(pk=uid).update(**form.cleaned_data, note=note)
            else:
                User.objects.filter(pk=uid).update(**form.cleaned_data)
            return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = "400"
    res["msg"] = "数据异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def staff_del(request):
    """删除员工"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    uid = request.POST.get("uid")
    c_obj = User.objects.filter(pk=uid).first()
    if c_obj:
        User.objects.filter(pk=uid).delete()

        return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = 400
    res["msg"] = "用户信息异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def staff_change_pwd(request):
    """修改密码"""
    res = {
        "status": 200,
        "msg": "添加成功"
    }
    pwd1 = request.POST.get("pwd1")
    pwd2 = request.POST.get("pwd2")
    if pwd1 != pwd2:
        res["status"] = "400"
        res["msg"] = "两次密码不相等"
        return HttpResponse(json.dumps(res), content_type="application/json")

    if not pwd1:
        res["status"] = "400"
        res["msg"] = "密码不能为空"
        return HttpResponse(json.dumps(res), content_type="application/json")

    uid = request.POST.get("uid")
    if not uid:
        res["status"] = "400"
        res["msg"] = "uid异常"
        return HttpResponse(json.dumps(res), content_type="application/json")
    form = forms.UserChangePwdForm({"password": pwd1})
    if form.is_valid():
        pwd = gen_pwd(pwd1)
        User.objects.filter(pk=uid).update(password=pwd)
        return HttpResponse(json.dumps(res), content_type="application/json")
    res["status"] = "400"
    res["msg"] = "数据异常"
    return HttpResponse(json.dumps(res), content_type="application/json")


def showmsg(request):
    """显示操作记录"""
    res = {
        "status": 200,
        "msg": "查询成功"
    }
    t_objs = Tis.objects.all().order_by("-id")

    page = request.GET.get("page", 1)
    p = Pagination(t_objs.count(), page, 6)
    t_objs = t_objs[p.start: p.end]
    page_li = p.page_str("javascript:void(0);", javaScriptMode=True)
    data = []
    unread = 0
    for t in t_objs:
        temp = {
            "operator": t.operator.username,
            "level": t.level,
            "read_msg": t.read_msg,
            "action": t.action,
            "operator_time": datetime.datetime.strftime(t.operator_time, "%Y-%m-%d %H:%M:%S")
        }
        if t.customer:
            temp["customer"] = t.customer.username
        else:
            temp["customer"] = "已删除"
        if not t.read_msg:
            unread += 1
        data.append(temp)
        # 设置为已读取
        t.read_msg = True
        t.save()
    res["data"] = data
    res["unread"] = unread
    res["page_li"] = page_li
    return HttpResponse(json.dumps(res), content_type="application/json")

