# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-13 04:20
from __future__ import unicode_literals

from django.db import migrations, models
import selstagram_server.model_mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawlJob',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('InProgress', 'InProgress'), ('Success', 'Success'), ('Fail', 'Fail')], max_length=32)),
                ('params', models.CharField(max_length=512)),
                ('tag', models.CharField(max_length=256)),
            ],
            options={
                'abstract': False,
            },
            bases=(selstagram_server.model_mixins.StringHelperModelMixin, models.Model),
        ),
    ]
