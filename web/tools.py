# # Create your tests here.
import random
import time
import datetime
from faker import Faker

from pytz import timezone

tz = timezone("Asia/Shanghai")

fake = Faker(locale='zh_CN')


def random_create_payment_customer(Customer, count=500):
    # 随机生成用户，需要第三方库Faker
    # 在views中的函数中使用即可
    random.seed(time.time())
    for _ in range(count):
        if random.randint(1, 10) > 3:
            is_payment = True
        else:
            is_payment = False
        t1 = datetime.datetime.now(tz)
        t = t1 - datetime.timedelta(days=random.randint(0, 7))
        name = fake.name()
        addr = fake.city()
        phone_number = fake.phone_number()
        money = 0
        play_time = None
        if is_payment:
            money = 8000
            play_time = t

        Customer.objects.create(username=name, money=money, create_time=t, play_time=play_time, addr=addr,
                                phone_number=phone_number)
