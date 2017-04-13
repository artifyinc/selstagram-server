#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import CrawlJob


class CrawlJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlJob
        fields = ('tag', 'limit_count')
