#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import InstagramMedia, Tag, DailyRank


class InstagramMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstagramMedia
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class DailyRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRank
        fields = '__all__'
        depth = 1


class RankSerializer(serializers.Serializer):
    date = serializers.DateField()
    rank = DailyRankSerializer(many=True)
