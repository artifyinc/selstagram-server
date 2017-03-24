#!/usr/bin/python
# -*- coding: utf-8 -*-

from selsta101 import factories as selsta101_factories
from selsta101 import models as selsta101_models


class InstagramMediaMixin(object):
    def create_instagram_media(self, size, **kwargs):
        if selsta101_models.Tag.objects.count() == 0:
            selsta101_factories.TagFactory.create()

        selsta101_factories.InstagramMediaFactory.create_batch(size, **kwargs)

    def create_tags(self, size, **kwargs):
        selsta101_factories.TagFactory.create_batch(size, **kwargs)

