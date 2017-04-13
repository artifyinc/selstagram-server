#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from dateutil.relativedelta import relativedelta
from django.core.management import BaseCommand
from django.db import transaction
from django_pandas.io import read_frame

from selsta101 import models as selsta101_models
from selstagram_server import utils

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    DEFAULT_TAG = '셀스타그램'

    def add_arguments(self, parser):
        parser.add_argument('--tag', action='store', default=Command.DEFAULT_TAG, help='tag name to crawl')
        parser.add_argument('--interval', action='store', help='interval in minutes', required=True)

    def setup_scheduler(self, tag, interval):
        self.executor = ThreadPoolExecutor(1)
        self.scheduler = BlockingScheduler(executors={'default': self.executor},
                                           timezone=utils.BranchUtil.SEOUL_TIMEZONE)

        job = self.scheduler.add_job(Command.rank,
                                     args=[tag],
                                     trigger='interval',
                                     next_run_time=(utils.BranchUtil.now() + relativedelta(seconds=5)),
                                     max_instances=1,
                                     minutes=interval)
        return job

    def handle(self, *args, **options):
        tag = options['tag']
        if tag is None:
            tag = Command.DEFAULT_TAG

        interval = int(options['interval'])

        self.setup_scheduler(tag, interval)
        self.scheduler.start()

    RUN_COUNT = 1

    @classmethod
    def rank(cls, tag, date=None):

        print("[{time}] Running Rank command.".format(time=utils.BranchUtil.now()))
        tag_object, created = selsta101_models.Tag.objects.get_or_create(name=tag)

        if created:
            # Empty data for the tag
            return []

        if date is None:
            date = utils.BranchUtil.today()

        last_rank = selsta101_models.DailyRank.objects.last()
        if not last_rank:
            this_time = 1
            Command.RUN_COUNT = 1
        else:
            if Command.RUN_COUNT != last_rank.turn:
                Command.RUN_COUNT = last_rank.turn

            this_time = last_rank.turn + 1

        print("[turn={turn}]".format(turn=Command.RUN_COUNT))
        rank_df = cls.get_daily_rank(date)

        with transaction.atomic():
            rank = 1
            daily_ranks = []
            for index, row in rank_df.iterrows():
                daily_rank = selsta101_models.DailyRank.objects.create(date=date,
                                                                       turn=this_time,
                                                                       rank=rank,
                                                                       media_id=index)
                daily_ranks.append(daily_rank)
                rank += 1

        print(rank_df[0:20])
        print("[{time}][{turn}] Rank command finished."
              .format(time=utils.BranchUtil.now(), turn=Command.RUN_COUNT))
        Command.RUN_COUNT += 1

        return daily_ranks

    @classmethod
    def get_daily_rank(cls, date):
        '''
            extract the ranking on the day of date (right to .75 percentile)
        :param date:
        :return: rank_df
        '''
        queryset = selsta101_models.InstagramMedia.objects.filter(created__date=date)
        media_df = read_frame(queryset,
                              fieldnames=('like_count', 'comment_count', 'votes'),
                              index_col='id')
        like_series = media_df['like_count']
        like_count_of_seventy_five_percentile = like_series.quantile(0.75)
        rank_df = media_df.loc[media_df.like_count >= like_count_of_seventy_five_percentile] \
            .sort_values(by=['like_count'], ascending=False)

        return rank_df
