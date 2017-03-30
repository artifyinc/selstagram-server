#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.pagination import LimitOffsetPagination, _get_count

from selsta101.models import InstagramMedia
from selstagram_server import utils


class InstagramMediaPageNation(LimitOffsetPagination):
    default_limit = 50

    def paginate_queryset(self, queryset, request, view=None):
        self.limit = self.get_limit(request)
        if self.limit is None:
            return None

        self.count = _get_count(queryset)
        self.request = request

        offset = self.get_offset(request)

        first_media_in_today = InstagramMedia.objects.filter(source_date__date=utils.BranchUtil.today()).first()
        self.offset = max(offset, first_media_in_today.id - 1) if first_media_in_today else offset

        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])
