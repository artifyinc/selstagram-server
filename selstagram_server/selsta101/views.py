from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import InstagramMediaSerializer
from .models import InstagramMedia


class InstagramMediaViewSet(viewsets.ModelViewSet):
    queryset = InstagramMedia.objects.all()
    serializer_class = InstagramMediaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


