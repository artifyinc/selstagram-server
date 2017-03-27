import json
import logging
import os

import itunesiap
import requests
from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from selsta101.pagenation import InstagramMediaPageNation
from selstagram_server import utils
from .models import InstagramMedia, Tag, DailyRank
from .serializers import InstagramMediaSerializer, TagSerializer, RankSerializer

log = logging.getLogger(__name__)


class InstagramMediaViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramMediaSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = InstagramMediaPageNation
    lookup_field = 'id'

    def get_queryset(self):
        return InstagramMedia.objects.order_by('id').all()

    def list(self, request, tag_name=None):
        queryset = self.get_queryset()

        if tag_name:
            queryset = queryset.filter(tag__name=tag_name)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @list_route()
    def recent(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @list_route()
    def popular(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @list_route()
    def rank(self, request, *args, **kwargs):
        daily_ranks_for_a_week = []

        now = utils.BranchUtil.now()
        queryset = self.get_queryset()

        for i in range(0, 7):
            date = (now - relativedelta(days=i)).date()
            daily_queryset = queryset.filter(source_date__date=date).order_by('-votes')
            count = daily_queryset.count()

            if count > 0:
                size = min(count, 101)
                daily_rank = {'date': date,
                              'rank': [DailyRank(date=date, rank=index + 1, media=instagram_media)
                                       for index, instagram_media in
                                       enumerate(daily_queryset[0:size])]}
                daily_ranks_for_a_week.append(daily_rank)

        serializer = RankSerializer(daily_ranks_for_a_week, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def vote(self, request, id=None):
        if not id:
            return Response(data="id is null", status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            instagram_media = InstagramMedia.objects.select_for_update().get(id=id)
            instagram_media.votes += 1
            instagram_media.save()

            return Response(status=status.HTTP_201_CREATED)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination
    queryset = Tag.objects.all()
    lookup_field = 'name'


@csrf_exempt
def verify_receipt(request):
    payload = json.loads(str(request.body, 'utf-8'))
    receipt_data = payload["receipt-data"]
    if payload.get("new", None):
        product_identifier = payload["new"]["productIdentifier"]
        requests.post(url=os.environ['SELSTA101_SLACK_INCOMING_HOOK_URL'],
                      json={"text": "New Customer: " + product_identifier})
    code, expires_date_ms = _verify_itunes_receipt(receipt_data=receipt_data)
    return JsonResponse({"code": code, "expires_date_ms": expires_date_ms})


def _verify_itunes_receipt(receipt_data):
    expires_date_ms = "0"
    code = 200
    itunes_shared_secret = os.environ['SELSTA101_ITUNES_SHARED_SECRET']

    try:
        with itunesiap.env.review:
            response = itunesiap.verify(receipt_data, itunes_shared_secret)
            in_apps = response.receipt.in_app
            for i in in_apps:
                new_expires_date_ms = i["expires_date_ms"]
                if int(new_expires_date_ms) > int(expires_date_ms):
                    expires_date_ms = new_expires_date_ms
    except itunesiap.exc.InvalidReceipt:
        code = 400
        log.error("invalid receipt")
    except itunesiap.exc.ItunesServerNotAvailable:
        code = 444
        log.error("ItunesServiceNotAvailable")
    except itunesiap.exc.ItunesServerNotReachable:
        code = 408
        log.error("iTunesServerNotReachable")
    except Exception:
        code = 500
        log.error("Unexpected error, itunesiap")

    if code == 500:
        """This case is a bug in itunesiap module on rare. It will be working to try once again."""
        return _verify_itunes_receipt(receipt_data)

    return code, expires_date_ms
