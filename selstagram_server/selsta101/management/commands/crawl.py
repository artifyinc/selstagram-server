#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import logging

from django.core.management import BaseCommand
from instaLooter.core import InstaLooter
from instaLooter.utils import get_times_from_cli, get_times

from selsta101 import models as selsta101_models
from selstagram_server import utils

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    # instagram hashtag crawler
    def add_arguments(self, parser):
        parser.add_argument('--tag', action='store', default='selfie', help='tag name to crawl')
        parser.add_argument('--time', action='store', help='(2017-03-03:2017-03-03)')
        parser.add_argument('--credential', action='store', help='my_insta_id:my_password', required=True)
        parser.add_argument('--count', action='store',
                            help='number of photos to crawl. IF NOT, all tagged photo are crawled')

    def handle(self, *args, **options):
        tag = options['tag']

        self.instagram_crawler = InstagramCrawler(directory=None,
                                                  profile=None,
                                                  hashtag=tag,
                                                  add_metadata=False,
                                                  get_videos=False,
                                                  videos_only=False)

        count = options.get('count', None)
        if count:
            count = int(count)

        credential = options['credential']
        username, password = credential.split(':')
        self.instagram_crawler.login(username, password)

        time_string = options['time']
        if time_string is None:
            yesterday_string = utils.BranchUtil.yesterday().isoformat()
            time_string = ':'.join([yesterday_string, yesterday_string])

        timeframe = get_times_from_cli(time_string)

        tag_object, created = selsta101_models.Tag.objects.get_or_create(name=tag)

        for media in self.instagram_crawler.medias(media_count=count,
                                                   timeframe=timeframe):
            # FIXME
            # insert_bulk
            # update_bulk

            source_date = datetime.datetime.fromtimestamp(media['date'],
                                                          tz=utils.BranchUtil.SEOUL_TIMEZONE)
            instagram_media, created = selsta101_models. \
                InstagramMedia.objects.get_or_create(tag=tag_object,
                                                     source_id=media['id'],
                                                     source_url=media['display_src'],
                                                     source_date=source_date,
                                                     code=media['code'],
                                                     width=media['dimensions']['width'],
                                                     height=media['dimensions']['height'],
                                                     thumbnail_url=media['thumbnail_src'],
                                                     owner_id=media['owner']['id'],
                                                     caption=media.get('caption', ''),
                                                     comment_count=media['comments']['count'],
                                                     like_count=media['likes']['count'],
                                                     )

            if not created:
                instagram_media.comment_count = media['comments']['count']
                instagram_media.like_count = media['likes']['count']
                instagram_media.save()

            logger.info(instagram_media.id, instagram_media.code, instagram_media.source_url, instagram_media.caption[0:20])


class InstagramCrawler(InstaLooter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def medias(self, media_count=None, with_pbar=False, timeframe=None):
        """An iterator over the media nodes of a profile or hashtag.

        Using :obj:`InstaLooter.pages`, extract media nodes from each page
        and yields them successively.

        Arguments:
            media_count (`int`): how many media to show before
                stopping **[default: None]**
            with_pbar (`bool`): display a progress bar **[default: False]**
            timeframe (`tuple`): a couple of datetime.date object
                specifying the date frame within which to yield medias
                (a None value can be given as well) **[default: None]**
                **[format: (start, stop), stop older than start]**

        """
        return super().medias(media_count=media_count,
                              with_pbar=with_pbar,
                              timeframe=timeframe)

    def _timeless_medias(self, media_count=None, with_pbar=False):
        count = 0

        if media_count == 0:
            return

        for page in self.pages(media_count=media_count, with_pbar=with_pbar):
            for media in page['entry_data'][self._page_name][0][self._section_name]['media']['nodes']:
                yield media

                count += 1
                if count >= media_count:
                    return

    def _timed_medias(self, media_count=None, with_pbar=False, timeframe=None):
        count = 0

        if media_count == 0:
            return

        start_time, end_time = get_times(timeframe)
        for page in self.pages(media_count=media_count, with_pbar=with_pbar):
            for media in page['entry_data'][self._page_name][0][self._section_name]['media']['nodes']:
                media_date = datetime.date.fromtimestamp(media['date'])
                if start_time >= media_date >= end_time:
                    yield media
                    count += 1

                elif media_date < end_time:
                    return

                if count >= media_count:
                    return
