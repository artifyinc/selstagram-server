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
        # Given :
        size = 10
        factories.InstagramMediaFactory.create_batch(size=size)

        # When :
        response = self.client.get('/media/')

        # Then :
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), size)

    def test_serializer(self):
        # Given:
        size = 10
        factories.InstagramMediaFactory.create_batch(size=size)

        # When :
        queryset = models.InstagramMedia.objects.all()
        serializer = serializers.InstagramMediaSerializer(queryset, many=True)

        json_renderer = renderers.JSONRenderer()
        response = json_renderer.render(serializer.data)

        # Then :
        print(response)

        self.fail()


