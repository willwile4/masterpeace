# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 17:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp_app', '0014_auto_20170505_0328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dob',
        ),
    ]
