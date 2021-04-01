# from scrapy.crawler import CrawlerRunner ,CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import os
# # from icrawler.spiders import bloomberght
# from icrawler.icrawler.spiders import bloomberght
# from icrawler.icrawler.spiders import milliyetKap
# from crochet import setup
#
#
#
# class Scraper:
#     def __init__(self):
#
#         settings_file_path = 'icrawler.icrawler.settings' # The path seen from root, ie. from main.py
#         os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
#         self.settings = get_project_settings()
#         self.process = CrawlerProcess(self.settings)
#         self.spider_bloomberg = bloomberght.BloombergSpider # The spider you want to crawl
#         self.spider_milliyetKAp = milliyetKap.MilliyetkapSpider # The spider you want to crawl
#
#     def run_spiders(self):
#         # self.setup()
#         self.process.crawl(self.spider_bloomberg)
#         self.process.start(self.spider_bloomberg)
#         # self.process.crawl(self.spider_milliyetKAp)
#
#         # self.process.start()  # the script will block here until the crawling is finished
#         # self.process.crawl()  # the script will block here until the crawling is finished

#
#
# class Scraper:
#     def __init__(self):
#
#         settings_file_path = 'icrawler.icrawler.settings' # The path seen from root, ie. from main.py
#         os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
#
#         self.settings = get_project_settings()
#         self.runner = CrawlerRunner(self.settings)
#         self.process = CrawlerProcess(self.settings)
#         self.spider_bloomberg = bloomberght.BloombergSpider # The spider you want to crawl
#         self.spider_milliyetKAp = milliyetKap.MilliyetkapSpider # The spider you want to crawl
#
#         self.process2 = CrawlerRunner(self.settings).create_crawler(self.spider_bloomberg)
#
#     def run_spiders(self):
#         # self.setup()
#         self.runner.crawl(self.spider_milliyetKAp)
#         self.process.crawl(self.spider_milliyetKAp)
#
#         # self.process.crawl(self.spider_milliyetKAp)
#
#         # self.process.start()  # the script will block here until the crawling is finished
#         # self.process.crawl()  # the script will block here until the crawling is finished
#
#

# PİPELİNE ÇALIŞMAYAN VERSİON
# import os
#
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from icrawler.spiders import bloomberght
# from icrawler.spiders import milliyetKap
#
#
# class Scraper:
#     def __init__(self):
#         configure_logging()
#         settings_file_path = 'icrawler.icrawler.settings'  # The path seen from root, ie. from main.py
#         os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
#         self.runner = CrawlerRunner()
#         self.spider_bloomberg = bloomberght.BloombergSpider
#         self.spider_milliyetKap = milliyetKap.MilliyetkapSpider
#
#     @defer.inlineCallbacks
#     def crawl(self):
#         yield self.runner.crawl(self.spider_bloomberg)
#         yield self.runner.crawl(self.spider_milliyetKap)
#         reactor.stop()
#
#     @staticmethod
#     def run_spiders():
#
#         reactor.run()
#
# if __name__ == '__main__':
#     s = Scraper()
#     s.crawl()
#     s.run_spiders()
import sys
from datetime import time
from time import sleep

from twisted.internet import reactor

from icrawler.icrawler.spiders.bloomberght import BloombergSpider
from icrawler.icrawler.spiders.milliyetKap import MilliyetkapSpider
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.utils.project import get_project_settings
import os


# class Scraper:
#     def __init__(self):
#
#         settings_file_path = 'icrawler.icrawler.settings' # The path seen from root, ie. from main.py
#         os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
#         self.settings = get_project_settings()
#         self.process = CrawlerProcess(self.settings)
#         self.spiderBloomberg = BloombergSpider # The spider you want to crawl
#         self.spiderMillliyetKap = MilliyetkapSpider # The spider you want to crawl
#
#     def run_spiders(self):
#
#         self.process.crawl(self.spiderBloomberg)
#         # self.process.crawl(self.spiderMillliyetKap)
#
#         self.process.start()  # the script will block here until the crawling is finished


class Scraper:
    def __init__(self):
        settings_file_path = 'icrawler.icrawler.settings'  # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.settings = get_project_settings()
        self.runner = CrawlerRunner(get_project_settings())

        self.spiderBloomberg = BloombergSpider  # The spider you want to crawl
        self.spiderMillliyetKap = MilliyetkapSpider  # The spider you want to crawl

    def run_spiders(self):
        d = self.runner.crawl(self.spiderBloomberg)
        d.addBoth(sleep)
        reactor.run()
        # d.addBoth(lambda _: crawl(runner))
