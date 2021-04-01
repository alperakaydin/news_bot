# from icrawler.main import Scraper
#
# class superScraperClass():
#     def __init__(self):
#
#         self.scraper = Scraper()
#
#     def start(self):
#         self.scraper.run_spiders()
#
# def deneme():
#     s = superScraperClass()
#     s.start()
# if __name__ == '__main__':
#     s =superScraperClass()
#     s.start()
# ------------------
# from scrapy.utils.log import configure_logging
# import icrawler.main
# from icrawler import main
#
# if __name__ == '__main__':
#     configure_logging()
#     s = main.Scraper()
#     s.run_spiders()
#     print("done")

# ----------------
# from scrapy import spiderloader
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
# from scrapy.utils.project import get_project_settings
# from twisted.internet import reactor
#
#
# class Scraper:
#     def __init__(self):
#
#         self.runner = CrawlerRunner()
#         self.spider = spiderloader.SpiderLoader.from_settings(get_project_settings())
#
#     def run_spiders(self):
#         for spider_name in self.spider.list():
#             print(spider_name)
#             self.runner.crawl(spider_name)
#         d = self.runner.join()
#         d.addBoth(lambda _: reactor.stop())
#
#         # log.start(logfile="file.log", loglevel=log.DEBUG, crawler=crawler, logstdout=False)
#
#         reactor.run()
from importlib import import_module

from crochet import setup
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

setup()
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_bot.settings")
import django
django.setup()

from _rss_bundler import rss2

from icrawler import run_out_scrapy
def rss_shedule_job():
    #  Your job processing logic here...
    # setup()
    print("rss_shedule_job")
    rss2.run_rss_schedular()


    # İCRAWLER
from icrawler.run_out_scrapy import Scraper
# scraper = Scraper()
# scraper.run_spiders()
def scrapy_shedule_job():
    setup()
    scraper = Scraper()
    scraper.run_spiders()

                         #from Scrapy docs
if __name__ == '__main__':
    scrapy_shedule_job()
    # rss2.run_rss_schedular()

    # print("start")
    # configure_logging()
    # s = Scraper()
    # s.run_spiders()
    # # TODO : burada bişeyler yap

