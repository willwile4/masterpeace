# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 20:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp_app', '0018_merge_20170506_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagemp',
            name='feedback1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagemp',
            name='feedback2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagemp',
            name='feedback3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagemp',
            name='feedback4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagemp',
            name='feedback5',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='feedback1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='feedback2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='feedback3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='feedback4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='feedback5',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textmp',
            name='text',
            field=models.TextField(blank=True, max_length=10000000, null=True),
        ),
    ]
