# Generated by Django 3.2.4 on 2021-06-28 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20210628_1906'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='pwd',
            new_name='password',
        ),
    ]
