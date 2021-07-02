from django.shortcuts import render, redirect
from django.utils.deprecation import MiddlewareMixin
import json
from EasyPermission import settings_doc
from EasyPermission.easyPermission import EasyPermission


# 不需要验证的视图
exclude_list = ["/", "/web/login"]
# 需要验证的视图
filter_list = ["/coustomer/list/", "/payment/list/", "/payment/add/", "/payment/edit/",
               "/payment/del/", "/staff/list/", "/  staff/add/", "/staff/edit/", "/staff/del/",
               "/staff/changpwd/", "/showmsg/"]



class AuthUserMiddleWare(MiddlewareMixin):
    """检验用户权限"""

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        在执行试图函数之前，加入session中有值，则被允许访问
        :return:
        """
        config = settings_doc
        easy_perm = EasyPermission(config)

        path = request.path
        if path in filter_list and path not in exclude_list:
            auth_user_id = easy_perm.get_user_func(request)  # 获取用户的ID
            if not auth_user_id:  # 没有用户id，要求登录
                return redirect(easy_perm.settings.get("LOGIN_PATH_URL"))
            # 已经登录，获取permission_list
            permission_list = request.session.get("permission_list")
            if permission_list is None:
                del request.session["user_data"]  # 删除user_id, 要求重新登录
                return redirect(easy_perm.settings.get("LOGIN_PATH_URL") + "?next=%s" % request.path)
            permission_list = json.loads(request.session["permission_list"])
            if permission_list == []:
                return render(request, easy_perm.settings.get("NOT_PERMISSION_PAGE_URL"),
                              status=403)  # 没有权限访问的提示页面


            if not easy_perm.handle(request, auth_user_id, permission_list=permission_list):
                return render(request, easy_perm.settings.get("NOT_PERMISSION_PAGE_URL"),
                              status=403)  # 没有权限访问的提示页面



