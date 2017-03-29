from django.test import TestCase

from selstagram_server import utils
from .management.commands.crawl import InstagramCrawler


class InstagramCrawlerTest(TestCase):
    def test_instagram_crawler(self):
        # Given : login to Instagram as username 'your_username'
        username = 'your_username'
        password = 'your_password'
        tag = 'selfie'
        crawler = InstagramCrawler(directory=None,
                                   profile=None,
                                   hashtag=tag,
                                   add_metadata=False,
                                   get_videos=False,
                                   videos_only=False)

        self.assertRaises(ValueError, crawler.login, username, password)

        # FIXME
        # After edit username, password value above,
        # remove # mark for code below and comment out code above assertion

        # crawler.login(username, password)
        #
        # # When : Crawling 40 instagram today's photos tagged by selfie
        # today = utils.BranchUtil.today()
        # count = 40
        #
        # number_of_media = 0
        # for _ in crawler.medias(media_count=count, timeframe=(today, today)):
        #     number_of_media += 1
        #
        # # Then : number of photos crawled is 40
        # self.assertEqual(count, number_of_media)
