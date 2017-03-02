# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 21:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0006_auto_20170301_1933'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='s_fname',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AddField(
            model_name='order',
            name='s_lname',
            field=models.CharField(default=None, max_length=60),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
