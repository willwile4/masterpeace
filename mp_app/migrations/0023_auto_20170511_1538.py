# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-11 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mp_app', '0022_abusiveimagereport_abusivetextreport'),
    ]

    operations = [
        migrations.AddField(
            model_name='abusiveimagereport',
            name='reported',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='abusivetextreport',
            name='reported',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
