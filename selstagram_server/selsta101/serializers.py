#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import InstagramMedia, Tag


class InstagramMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMedia
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
