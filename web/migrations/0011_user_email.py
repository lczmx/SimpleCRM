# Generated by Django 3.2.4 on 2021-07-01 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20210630_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='abc@qq.com', max_length=32),
            preserve_default=False,
        ),
    ]
