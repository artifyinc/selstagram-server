#!/usr/bin/python
# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from selsta101 import factories as selsta101_factories
from selsta101 import models as selsta101_models
from selstagram_server import utils


class InstagramMediaMixin(object):
    def create_instagram_media(self, size, **kwargs):
        if selsta101_models.Tag.objects.count() == 0:
            selsta101_factories.TagFactory.create()

        selsta101_factories.InstagramMediaFactory.create_batch(size, **kwargs)

    def create_tags(self, size, **kwargs):
        selsta101_factories.TagFactory.create_batch(size, **kwargs)

    def create_ranks(self):
        self.create_tags(1)

        today = utils.BranchUtil.now()
        for i in range(6, -1, -1):
            date = today - relativedelta(days=i)
            self.create_instagram_media(101, source_date=date)



