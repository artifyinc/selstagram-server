import json

from django.http import HttpRequest
from django.test import TestCase
from munch import Munch
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.test import APITestCase

from selsta101.views import InstagramMediaPageNation
from selstagram_server import utils, test_mixins
from . import models as selsta101_models


class MediaViewTests(test_mixins.InstagramMediaMixin, APITestCase):
    def setUp(self):
        pass

    def test_tags(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_tags(size)

        # When : Invoking media api
        response = self.client.get('/tags/')

        # Then : LimitOffsetPagination.default_limit media elements must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        media_ = Munch(response.data)
        self.assertEqual(len(media_.results), LimitOffsetPagination.default_limit)

    def test_tags_tag_name(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_tags(size)

        tag_id = 3
        tag_name = selsta101_models.Tag.objects.get(id=tag_id).name

        # When : Invoking media api
        response = self.client.get('/tags/{tag_name}/'.format(tag_name=tag_name))

        # Then : LimitOffsetPagination.default_limit media elements must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        media_ = Munch(response.data)

        self.assertEqual(media_.id, tag_id)

    def test_media(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_instagram_media(size)

        # When : Invoking media api
        # response = self.client.get('/tags/{tag_name}/media/recent/'.format(tag_name='셀스타그램'))

        response = self.client.get('/tags/셀스타그램2/media/recent/')

        # Then : InstagramMediaPageNation.default_limit numbers of media must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        media_ = Munch(response.data)
        self.assertEqual(len(media_.results), InstagramMediaPageNation.default_limit)

    def test_media_pagenation_limit_offset(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_instagram_media(size)

        # When : Invoking media api with limit=100 and offset=37
        limit = 100
        offset = 37
        response = self.client.get('/tags/셀스타그램2/media/recent/'
                                   '?limit={limit}&offset={offset}'
                                   .format(limit=limit, offset=offset))

        # Then : 100 media elements of which ids are [38, 137] must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        media_ = Munch(response.data)
        self.assertEqual(len(media_.results), limit)

        ids = range(offset + 1, offset + limit + 1)
        self.assertEqual(len(ids), limit)
        self.assertSequenceEqual(ids,
                                 list(map(lambda item: item['id'], media_.results)))

    def test_media_pagenation_limit(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_instagram_media(size)

        # When : Invoking media api with limit=100
        limit = 100
        response = self.client.get('/tags/셀스타그램2/media/recent/'
                                   '?limit={limit}'.format(limit=limit))

        # Then : 100 media elements of which ids are [0, 99] must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        media_ = Munch(response.data)
        self.assertEqual(len(media_.results), limit)

        ids = range(1, limit + 1)
        self.assertEqual(len(ids), limit)

        self.assertSequenceEqual(ids, list(map(lambda item: item['id'], media_.results)))

    def test_media_pagenation_offset(self):
        # Given : Create 1000 dummy InstagramMedia
        size = 1000
        self.create_instagram_media(size)

        # When : Invoking media api with offset=37
        offset = 37
        response = self.client.get('/tags/셀스타그램2/media/recent/'
                                   '?offset={offset}'.format(offset=offset))

        # Then : The numbers of media received is as same as
        # InstagramMediaPageNation.default_limit
        default_limit = InstagramMediaPageNation.default_limit
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        media_ = Munch(response.data)
        self.assertEqual(len(media_.results), default_limit)

        ids = range(offset + 1, offset + default_limit + 1)
        self.assertEqual(len(ids), default_limit)
        self.assertSequenceEqual(ids, list(map(lambda item: item['id'], media_.results)))


class InstagramMediaPagenatorTest(test_mixins.InstagramMediaMixin, TestCase):
    def test_today_offset_reset(self):
        # Given: There are 1000 InstagramMedia crawled yesterday and 1000 InstagramMedia crawled today.
        size = 1000
        self.create_instagram_media(size,
                                    source_date=utils.BranchUtil.date_to_datetime(
                                        utils.BranchUtil.yesterday()))

        self.create_instagram_media(size,
                                    source_date=utils.BranchUtil.date_to_datetime(
                                        utils.BranchUtil.today()))

        self.assertEqual(selsta101_models.InstagramMedia.objects.count(), 2 * size)

        # When : pagenate queryset with offset=100
        request = HttpRequest()
        request.query_params = {'offset': 100}

        instagram_media_pagenator = InstagramMediaPageNation()
        pagenated_queryset = instagram_media_pagenator. \
            paginate_queryset(selsta101_models.InstagramMedia.objects.all(),
                              request)

        # Then : ids in pagenated queryset are [1001, 1001 + InstagramMediaPageNation.default_limit]
        self.assertEqual(pagenated_queryset[0].id, size + 1)
        self.assertEqual(pagenated_queryset[-1].id, size + InstagramMediaPageNation.default_limit)
        self.assertEqual(len(pagenated_queryset), InstagramMediaPageNation.default_limit)

    def test_today_offset(self):
        # Given: There are 1000 InstagramMedia crawled yesterday and 1000 InstagramMedia crawled today.
        size = 1000
        self.create_instagram_media(size,
                                    source_date=utils.BranchUtil.date_to_datetime(
                                        utils.BranchUtil.yesterday()))

        self.create_instagram_media(size,
                                    source_date=utils.BranchUtil.date_to_datetime(
                                        utils.BranchUtil.today()))

        self.assertEqual(selsta101_models.InstagramMedia.objects.count(), 2 * size)

        # When : pagenate queryset with offset=1600
        request = HttpRequest()
        offset = 1600
        request.query_params = {'offset': offset}

        instagram_media_pagenator = InstagramMediaPageNation()
        pagenated_queryset = instagram_media_pagenator. \
            paginate_queryset(selsta101_models.InstagramMedia.objects.all(),
                              request)

        # Then : ids in pagenated queryset are [1001, 1001 + InstagramMediaPageNation.default_limit]
        self.assertEqual(pagenated_queryset[0].id, offset + 1)
        self.assertEqual(pagenated_queryset[-1].id, offset + InstagramMediaPageNation.default_limit)
        self.assertEqual(len(pagenated_queryset), InstagramMediaPageNation.default_limit)


class CrawlCommandTests(TestCase):
    def test_crawl_command(self):
        # # Given :
        # number_of_media_before_crawling = models.InstagramMedia.objects.count()
        #
        # # When : crawls 15 photos tagged by selfie from Instagram
        # count = 15
        # out = StringIO()
        # call_command('crawl',
        #              tag='selfie',
        #              time='thisday',
        #              credential='your_username:your_password',
        #              count=count,
        #              stdout=out)
        #
        # # Then : 15 InstagramMedia are added
        # number_of_media_after_crawling = models.InstagramMedia.objects.count()
        #
        # self.assertEqual(number_of_media_before_crawling + 15, number_of_media_after_crawling)
        pass
