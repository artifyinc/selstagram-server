# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-21 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramMedia',
            fields=[
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('collected_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tag', models.CharField(max_length=128)),
                ('source_id', models.BigIntegerField()),
                ('source_url', models.URLField(max_length=256)),
                ('code', models.CharField(max_length=64)),
                ('width', models.PositiveSmallIntegerField()),
                ('height', models.PositiveSmallIntegerField()),
                ('thumbnail_url', models.URLField(max_length=256)),
                ('owner_id', models.BigIntegerField()),
                ('caption', models.TextField()),
                ('comment_count', models.PositiveIntegerField()),
                ('like_count', models.PositiveIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]