from django.forms import ModelForm
from . import models


class CustomerForm(ModelForm):
    class Meta:
        fields = ["username", "addr", "money", "phone_number"]
        model = models.Customer


class UserForm(ModelForm):
    class Meta:
        fields = ["email", "username", "password"]
        model = models.User


class UserChangeForm(ModelForm):
    class Meta:
        fields = ["username"]
        model = models.User


class UserChangePwdForm(ModelForm):
    class Meta:
        fields = ["password"]
        model = models.User
