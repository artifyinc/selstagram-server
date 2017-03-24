#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta
from django.utils import timezone as django_timezone
from pytz import timezone as pytz_timezone


class BranchUtil(object):
    SEOUL_TIMEZONE = pytz_timezone('Asia/Seoul')
    UTC = pytz_timezone('UTC')

    @staticmethod
    def yesterday():
        return BranchUtil.today() + relativedelta(days=-1)

    @staticmethod
    def today():
        return BranchUtil.now().date()

    @staticmethod
    def tomorrow():
        return BranchUtil.today() + relativedelta(days=1)

    @staticmethod
    def now():
        now = django_timezone.now()
        return BranchUtil.to_seoul(now)

    @classmethod
    def date_to_datetime(cls, date):
        return cls.localize(datetime.datetime.combine(date, datetime.time.min))

    @classmethod
    def localize(cls, dt):
        return cls.SEOUL_TIMEZONE.localize(dt)

    @classmethod
    def to_utc(cls, dt=None):
        if dt is None:
            dt = BranchUtil.now()

        return dt.astimezone(cls.UTC)

    @classmethod
    def to_seoul(cls, dt):
        return dt.astimezone(cls.SEOUL_TIMEZONE)

    @classmethod
    def calc_utc_min_max_datetime(cls, date=None):
        if date is None:
            date = BranchUtil.today()

        dt = cls.date_to_datetime(date)
        from_datetime = datetime.datetime.combine(dt.date(), datetime.time.min)
        from_datetime = cls.localize(from_datetime)
        from_datetime = cls.to_utc(from_datetime)

        to_datetime = datetime.datetime.combine(dt.date(), datetime.time.max)
        to_datetime = cls.localize(to_datetime)
        to_datetime = cls.to_utc(to_datetime)

        return from_datetime, to_datetime
