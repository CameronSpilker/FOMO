# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-08 00:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20170307_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.TextField(blank=True, null=True),
        ),
    ]
