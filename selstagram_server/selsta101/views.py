import json
import logging
import os

import itunesiap
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework import viewsets

from selsta101.pagenation import InstagramMediaPageNation
from .models import InstagramMedia
from .serializers import InstagramMediaSerializer

log = logging.getLogger(__name__)


class InstagramMediaViewSet(viewsets.ModelViewSet):
    serializer_class = InstagramMediaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    pagination_class = InstagramMediaPageNation
    queryset = InstagramMedia.objects.order_by('id').all()


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
                if new_expires_date_ms > expires_date_ms:
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
