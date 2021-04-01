# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IcrawlerItem(scrapy.Item):
    source = scrapy.Field()
    title= scrapy.Field()
    category= scrapy.Field()
    description= scrapy.Field()
    pubDate= scrapy.Field()
    link= scrapy.Field()
    thumbnail_url= scrapy.Field()
    is_company_news= scrapy.Field()
    company_code= scrapy.Field()
    extra_field= scrapy.Field()

    # item["source"]
    # item['title']
    # item['category']
    # item['pubDate']
    #
    # item['description']
    # item['link']
    # item['thumbnail_url']
    # item['is_company_news']
    # item['company_code']
    # item['extra_field']
