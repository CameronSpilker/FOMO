# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 22:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170329_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='shipping',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='sale',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.AddField(
            model_name='sale',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
    ]
