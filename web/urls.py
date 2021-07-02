from django.urls import path
from web import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),

    path("coustomer/list/",  views.customer_list, name="customer_list"),

    path("payment/list/",  views.payment_list, name="payment_list"),
    path("payment/add/",  views.payment_add, name="payment_add"),
    path("payment/edit/",  views.payment_edit, name="payment_edit"),
    path("payment/del/",  views.payment_del, name="payment_del"),

    path("staff/list/", views.staff_list, name="staff_list"),
    path("staff/add/", views.staff_add, name="staff_add"),
    path("staff/edit/", views.staff_edit, name="staff_edit"),
    path("staff/del/", views.staff_del, name="staff_del"),
    path("staff/changpwd/", views.staff_change_pwd, name="staff_change_password"),
    path("showmsg/", views.showmsg, name="showmsg"),

]