# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 01:20
from __future__ import unicode_literals

from django.db import migrations, models

import selstagram_server.utils


class Migration(migrations.Migration):

    dependencies = [
        ('selsta101', '0002_auto_20170322_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagrammedia',
            name='collected_at',
        ),
        migrations.RemoveField(
            model_name='instagrammedia',
            name='last_updated_at',
        ),
        migrations.AddField(
            model_name='instagrammedia',
            name='source_date',
            field=models.DateTimeField(default=selstagram_server.utils.BranchUtil.now),
        ),
        migrations.AlterField(
            model_name='instagrammedia',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='instagrammedia',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
