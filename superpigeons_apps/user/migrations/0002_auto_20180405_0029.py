# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-04 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userscore',
            name='score',
            field=models.IntegerField(),
        ),
    ]
