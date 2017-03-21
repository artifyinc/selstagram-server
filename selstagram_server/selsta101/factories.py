#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import factory

from .models import InstagramMedia


class InstagramMediaFactory(factory.DjangoModelFactory):
    created = datetime.date.fromtimestamp(1490058065)
    modified = datetime.date.fromtimestamp(1490058065)

    tag = u'selfie'
    source_id = 1475036421974990331
    source_url = 'https://scontent-hkg3-1.cdninstagram.com/t51.2885-15/e35/17332382_1671128616520693_6601783536213032960_n.jpg'

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
