# Generated by Django 2.2.4 on 2020-05-19 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0019_auto_20200519_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 19, 21, 54, 22, 642871), verbose_name='sendTime'),
        ),
    ]
