# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 02:47
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import selsta101.models


class Migration(migrations.Migration):

    dependencies = [
        ('selsta101', '0004_auto_20170324_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyRank',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(db_index=True)),
                ('rank', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=(selsta101.models.StringHelperModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='instagrammedia',
            name='votes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dailyrank',
            name='media',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='selsta101.InstagramMedia'),
        ),
    ]
