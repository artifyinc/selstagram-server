import time

from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TestCase

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

from .management.commands.crawl import InstagramCrawler

from selstagram_server import utils


class DummyClass(object):
    @classmethod
    def dummy_job(cls, time_to_sleep):
        print("Start dummy_job")
        time.sleep(time_to_sleep)
        print("End dummy_job")



class InstagramCrawlerTest(TestCase):
    def test_instagram_crawler(self):
        # Given : login to Instagram as username 'your_username'
        # username = 'your_username'
        # password = 'your_password'
        tag = 'selfie'
        crawler = InstagramCrawler(directory=None,
                                   profile=None,
                                   hashtag=tag,
                                   add_metadata=False,
                                   get_videos=False,
                                   videos_only=False)

        # self.assertRaises(ValueError, crawler.login, None)

        # FIXME
        # After edit username, password value above,
        # remove # mark for code below and comment out code above assertion

        # crawler.login(username, password)
        #
        # # When : Crawling 40 instagram today's photos tagged by selfie
        today = utils.BranchUtil.today()
        count = 40

        number_of_media = 0
        for _ in crawler.medias(media_count=count, timeframe=(today, today)):
            number_of_media += 1

        # Then : number of photos crawled is 40
        self.assertEqual(count, number_of_media)

    # def test_crawl_commad(self):
    #     # FIXME
    #     # After edit username, password value above,
    #     # remove # mark for code below and comment out code above assertion
    #     call_command("crawl",
    #                  "--interval=2",
    #                  # "--credential=your_account:your_password",
    #                  "--tag=셀스타그램",
    #                  # --time=start:stop
    #                  # stop is older than tsrt
    #                  # "--time=2017-04-04:2017-04-01",
    #                  "--count=24")

    # testing apscheduler usage
    # def test_apscheduler(self):
    #     executor = ThreadPoolExecutor(10)
    #     scheduler = BackgroundScheduler(executors={'default': executor},
    #                                     timezone=utils.BranchUtil.SEOUL_TIMEZONE)
    #
    #     interval = 4
    #
    #     scheduler.add_job(DummyClass.dummy_job,
    #                       args=[interval*2],
    #                       trigger='interval',
    #                       seconds=interval,
    #                       next_run_time=(utils.BranchUtil.now() + relativedelta(seconds=1)),
    #                       max_instances=3)
    #
    #     scheduler.start()
    #
    #     time.sleep(1000)
