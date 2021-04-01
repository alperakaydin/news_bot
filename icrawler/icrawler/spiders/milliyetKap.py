import scrapy
from ..items import IcrawlerItem
from datetime import datetime
from pytz import timezone
import re
class MilliyetkapSpider(scrapy.Spider):
    name = 'milliyetKap'
    allowed_domains = ['milliyet.com.tr']
    start_urls = ['https://uzmanpara.milliyet.com.tr/kap-haberleri/']

    def saat_ayarla(self, date):
        if date:

            dt_str = date.split()
            #print(dt_str[-1:][0])
            t_str = str(dt_str[-1:][0]).replace(":"," ").split()
            hour = int(t_str[0])
            minute = int(t_str[1])
            print(hour, minute)

            cst = datetime.now(timezone('europe/istanbul'))

            dt = datetime(cst.year,cst.month,cst.day,hour,minute)
            print(dt)

            return dt
        else:
            return None

    # 1. FOLLOWING LEVEL 1
    def parse(self, response):
        follows = response.xpath(".//ul[@class='newsUl newsUl3']/li/a[2]/@href").getall()

        for follow_url in follows:
            joined_url = response.urljoin(follow_url)

            yield response.follow(joined_url, self.populate_item )
        yield self.paginate(response)

    # 2. SCRAPING LEVEL 2
    def populate_item(self ,response  ):

        print(response.url)

        item = IcrawlerItem()


        title = response.xpath(".//div[@class='detTitle']/h1/text()").get()
        try:
            regex = "(?<=\*\*\*)(.*)(?=\*\*\*)"
            company_code_temp = re.search(regex, title, re.IGNORECASE)
            company_code = company_code_temp.group()
        except:
            company_code=""
        date = response.xpath(".//div[@class='detTitle']/span/text()").get()

        pubDate = self.saat_ayarla(date)
        text=""
        summary = response.xpath(".//div[@class='detL']/text()").getall() #[position()<last()]
        for sum in summary:
            text = text + "\n" + sum


        item["source"] = 'milliyet-kap'
        item['title'] = title
        item['category'] = 'sirket'
        item['pubDate'] = pubDate

        item['description'] = text.strip()
        item['link'] = response.url
        item['thumbnail_url'] = ""
        item['is_company_news'] = True


        item['company_code'] = company_code
        item['extra_field'] = ""
        yield item

    # 3. PAGINATION LEVEL 1
    def paginate(self, response):
        next_page_url = response.css('li.next > a::attr(href)').extract_first()  # pagination("next button") <a> element here


        next_page_url = response.urljoin(next_page_url)


        if next_page_url is not None:
            return response.follow(next_page_url, self.parse)