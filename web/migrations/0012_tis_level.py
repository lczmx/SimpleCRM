# Generated by Django 3.2.4 on 2021-07-01 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='tis',
            name='level',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]