# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selsta101', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagrammedia',
            name='source_id',
            field=models.BigIntegerField(db_index=True),
        ),
    ]
