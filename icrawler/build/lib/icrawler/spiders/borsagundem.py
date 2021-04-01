import scrapy


class BorsagundemSpider(scrapy.Spider):
    name = 'borsagundem'
    allowed_domains = ['borsagundem.com']
    start_urls = ['http://borsagundem.com/']

    def parse(self, response):
        pass
