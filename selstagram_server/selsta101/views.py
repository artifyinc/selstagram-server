from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import InstagramMediaSerializer
from .models import InstagramMedia

import itunesiap
import json
import requests

import logging
log = logging.getLogger(__name__)


class InstagramMediaViewSet(viewsets.ModelViewSet):
    queryset = InstagramMedia.objects.all()
    serializer_class = InstagramMediaSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


@csrf_exempt
def verify_receipt(request):
    payload = json.loads(request.body)
    receipt_data = payload["receipt-data"]
    if payload.get("new", None):
        product_identifier = payload["new"]["productIdentifier"]
        requests.post(url="https://hooks.slack.com/services/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",
                      json={"text": "New Customer: " + product_identifier})
    code, expires_date_ms = _verify_itunes_receipt(receipt_data=receipt_data)

    return JsonResponse({"code": code, "expires_date_ms": expires_date_ms})


def _verify_itunes_receipt(receipt_data):
    expires_date_ms = 0
    code = 200
    try:
        with itunesiap.env.review:
            response = itunesiap.verify(receipt_data, "bd68c919a8824b7f9e2082a50e8a79b3")
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

    if code == 500:
        """This case is a bug in itunesiap module on rare. It will be working to try once again."""
        return _verify_itunes_receipt(receipt_data)

    return code, expires_date_ms
