#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import InstagramMedia


class InstagramMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMedia
        fields = '__all__'
