#!/usr/bin/python
# -*- coding: utf-8 -*-

import factory

from selstagram_server import utils
from .models import InstagramMedia, Tag


class TagFactory(factory.DjangoModelFactory):
    name = '셀스타그램'

    class Meta:
        model = Tag

    @factory.sequence
    def name(seq):
        tag_name = '셀스타그램'

        if Tag.objects.count() == 0:
            return tag_name
        else:
            return ''.join([tag_name, str(seq)])


class InstagramMediaFactory(factory.DjangoModelFactory):
    tag = factory.Iterator(Tag.objects.all())

    source_id = 1475036421974990331
    source_url = 'https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/17332382_1671128616520693_6601783536213032960_n.jpg'
    source_date = factory.LazyFunction(lambda: utils.BranchUtil.date_to_datetime(
        utils.BranchUtil.today()))

    code = 'BR4Yc-KlR37'
    width = 1349
    height = 1080

    thumbnail_url = 'https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/s640x640/sh0.08/e35/c0.134.1080.1080/17332382_1671128616520693_6601783536213032960_n.jpg'
    owner_id = 247272838

    caption = u'\u2600\ufe0f'
    comment_count = 47
    like_count = 2785

    class Meta:
        model = InstagramMedia
