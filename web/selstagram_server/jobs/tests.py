# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from selsta101 import models as selsta101_models


class CrawlJobTest(APITestCase):
    def setUp(self):
        pass

    def test_get_crawl_job_list(self):
        # Given:

        # When: get crawl job list
        response = self.client.get('/jobs/crawl/')

        # Then:
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_submit_crawl_job(self):
        # Given:
        number_of_media_before_crawl = selsta101_models.InstagramMedia.objects.count()

        # When: submit crawl job
        count = 50
        response = self.client.post('/jobs/crawl/', data={'limit_count': count, 'tag': '셀스타그램'})

        # Then:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        number_of_media_after_crawl = selsta101_models.InstagramMedia.objects.count()

        self.assertEqual(number_of_media_after_crawl, number_of_media_before_crawl + count)
