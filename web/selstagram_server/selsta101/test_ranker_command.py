#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.management import call_command
from django.test import TestCase

from selsta101.management.commands.rank import Command as RankCommand
from selstagram_server.test_mixins import InstagramMediaMixin
from selstagram_server.utils import BranchUtil


class RankerTest(InstagramMediaMixin, TestCase):

    def test_rank(self):
        # Given: There are 1000 medias
        size = 1000
        self.create_instagram_media(size)

        # When: getting daily rank
        date = BranchUtil.today()
        tag = '셀스타그램'
        ranks = RankCommand.rank(tag, date)

        # Then: id of rank_df is [1000, 998, 997, ..., 752, 751]
        self.assertListEqual([rank.media.id for rank in ranks], list(range(1000, 750, -1)))

    # def test_rank_command(self):
    #     size = 1000
    #     self.create_instagram_media(size)
    #
    #     call_command("rank",
    #                  "--interval=10",
    #                  "--tag=셀스타그램")
    #     self.fail()
