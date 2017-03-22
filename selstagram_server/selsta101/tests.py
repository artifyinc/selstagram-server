from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO
from rest_framework import status
from rest_framework.test import APITestCase

from . import factories
from . import models


class MediaViewTests(APITestCase):
    def setUp(self):
        pass

    def test_media(self):
        # Given : Create 10 dummy InstagramMedia
        size = 10
        factories.InstagramMediaFactory.create_batch(size=size)

        # When : Invoking media api
        response = self.client.get('/media/')

        # Then : 10 media elements must be received
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), size)


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
