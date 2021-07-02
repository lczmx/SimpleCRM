from django.contrib import admin
from .models import User, Customer, Tis
from EasyPermission.models import Role, Role2User, Action, Permission, Detail, Hooks, Action2Permission, \
    Action2Permission2Detail, Action2Permission2Hooks, Role2Action2Permission, User2Action2Permission, Menu


# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tis)
admin.site.register(Role)
admin.site.register(Role2User)
admin.site.register(Action)
admin.site.register(Permission)
admin.site.register(Detail)
admin.site.register(Hooks)
admin.site.register(Action2Permission)

admin.site.register(Action2Permission2Detail)
admin.site.register(Action2Permission2Hooks)
admin.site.register(Role2Action2Permission)
admin.site.register(User2Action2Permission)

admin.site.register(Menu)
admin.site.register(Customer)
