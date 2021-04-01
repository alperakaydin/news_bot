

# from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import os
# from icrawler.spiders import bloomberght
from icrawler.icrawler.spiders import bloomberght
from icrawler.icrawler.spiders import milliyetKap
from crochet import setup

class Scraper:
    def __init__(self):

        settings_file_path = 'icrawler.icrawler.settings' # The path seen from root, ie. from main.py
        os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
        self.process = CrawlerRunner(get_project_settings())
        self.spider_bloomberg = bloomberght.BloombergSpider # The spider you want to crawl
        self.spider_milliyetKAp = milliyetKap.MilliyetkapSpider # The spider you want to crawl

    def run_spiders(self):
        # self.setup()
        self.process.crawl(self.spider_bloomberg)
        # self.process.crawl(self.spider_milliyetKAp)

        # self.process.start()  # the script will block here until the crawling is finished
        # self.process.crawl()  # the script will block here until the crawling is finished



if __name__ == '__main__':
    s = Scraper()
    s.run_spiders()