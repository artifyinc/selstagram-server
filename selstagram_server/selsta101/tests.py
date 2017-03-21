from django.test import TestCase

# Create your tests here.
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import renderers

from . import factories
from . import serializers
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
