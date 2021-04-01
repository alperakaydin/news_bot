import scrapy
from datetime import datetime
from pytz import timezone
import time

from ..items import IcrawlerItem

class BloombergSpider(scrapy.Spider):



    name = 'bloomberg'
    allowed_domains = ['www.bloomberght.com']
    start_urls = ['https://www.bloomberght.com/tum-ekonomi-haberleri']

    def saat_ayarla(self, date):
        if date:

            dt_str = date.split()
            #print(dt_str[-1:][0])
            t_str = str(dt_str[-1:][0]).replace(":"," ").split()
            hour = int(t_str[0])
            minute = int(t_str[1])
            print(hour, minute)

            cst = datetime.now(timezone('europe/istanbul'))
            print(cst)

            print("---------")
            dt = datetime(cst.year,cst.month,cst.day,hour,minute)
            return dt
        else:
            return None


    def parse(self, response):
        #DjangoItem


        haberler = response.xpath("//div[@class='widget-news-list type1']/ul/li")
        for haber in haberler:

            item =IcrawlerItem()

            title = haber.xpath(".//a/@title").get()
            summary = haber.xpath(".//a/figure/figcaption/span[@class='description']/text()").get()
            link = haber.xpath(".//a/@href").get()
            img = haber.xpath(".//a/figure/span/img/@data-src").get()
            news_date = self.saat_ayarla(haber.xpath(".//a/figure/figcaption/span[@class='date']/text()").get())

            item["source"] ='bloomberght'
            item['title'] = title
            item['category'] = 'ekonomi'
            item['pubDate'] = news_date

            item['description'] = summary
            item['link'] = response.urljoin(link)
            item['thumbnail_url'] = img
            # item['is_company_news'] = False
            # item['company_code'] = None
            # item['extra_field'] = None

            yield item

