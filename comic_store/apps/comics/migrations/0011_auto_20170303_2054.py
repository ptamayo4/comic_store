# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0010_auto_20170303_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='street_two',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='pic_folder/default.jpg', upload_to='pic_folder/'),
        ),
    ]
