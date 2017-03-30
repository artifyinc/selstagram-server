#!/usr/bin/python
# -*- coding: utf-8 -*-

from celery import Celery
from celery.schedules import crontab
from django.core.management import call_command

celery_app = Celery('selstagram_server', backend='django-db')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
celery_app.autodiscover_tasks()


@celery_app.task
def crawl_instagram_tag(tag, count_limit, credential):
    args = [
        '--tag', tag,
        '--time', 'thisday',
        '--credential', credential,
        '--count', count_limit
    ]
    call_command('crawl', *args)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #     crontab(hour='*/2'),
    #     crawl_instagram_tag.s('셀스타그램', 80000, '3times3meals:selsta101!')
    # )

    sender.add_periodic_task(
        crontab(minute=19),
        crawl_instagram_tag.s('셀스타그램', 80000, '3times3meals:selsta101!')
    )
