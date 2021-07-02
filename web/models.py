from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

class User(models.Model):
    """职员表，放的是职员信息"""
    email = models.EmailField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    entry_time = models.DateTimeField()
    note = models.CharField(max_length=128, default="")

    def __str__(self):
        return self.username


class Customer(models.Model):
    """顾客表"""
    username = models.CharField(max_length=32)
    money = models.IntegerField(verbose_name="付费金额", default=0)
    create_time = models.DateTimeField()
    play_time = models.DateTimeField(default=None, blank=True, null=True)
    addr = models.CharField(max_length=64, verbose_name="家庭住址")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                     message="格式：'+999999999'. 最多15位数.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17,
                                        blank=True)

    def __str__(self):
        return self.username


class Tis(models.Model):
    """存放纪录操作"""
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=32)
    operator = models.ForeignKey(User, on_delete=models.CASCADE)
    read_msg = models.BooleanField(default=False)
    level = models.IntegerField()   # 1 正常操作 2 需要注意 3 警告
    operator_time = models.DateTimeField()

    def __str__(self):
        return f"{self.operator.username} -- {self.action}"
