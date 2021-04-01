# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
# import help_data
# import sqlite3
#
# class IcrawlerPipeline:
#     def __init__(self):
#         self.Base_Dır = help_data.get_base_dır()
#         self.create_connection()
#
#
#
#     def create_connection(self):
#         self.conn = sqlite3.connect(self.Base_Dır /  'db.sqlite3')
#         print("BAĞLANTI AÇILDIII --------------------------------------------------------------------------")
#         self.curr = self.conn.cursor()
#
#
#     def process_item(self, item, spider):
#         self.store_db(item)
#         return item
#
#     def store_db(self, item):
#         try:
#             self.curr.execute(
#                 """INSERT INTO news_news( source,title,category,subcategory,description,pubDate,link,thumbnail_url) VALUES (?,?,?,?,?,?,?,?)""", (
#                     item['source'],
#                     item['title'],
#                     item['category'],
#                     item['subcategory'],
#                     item['description'],
#                     item['pubDate'],
#                     item['link'],
#                     item['thumbnail_url'],
#                 ))
#             print("EXECUTE --------------------------------------------------------------------------")
#             self.conn.commit()
#         except:
#             print("KAYIT ZATEN MEVCUT")




from news.models import news

class IcrawlerPipeline(object):
    def process_item(self, item, spider):
        try:
            question = news.objects.get(link=item["link"])
            print("Haber zaten mevcut")

            return item
        except news.DoesNotExist:
            pass

        new = news()

        new.source = item["source"]
        new.title = item['title']
        new.category = item['category']
        new.pubDate = item['pubDate']

        new.description =  item['description']
        new.link= item['link']
        new.thumbnail_url= item['thumbnail_url']
        if 'is_company_news' in item:
            new.is_company_news= item['is_company_news']
            new.company_code= item['company_code']
            new.extra_field= item['extra_field']


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



        new.save()
        return item














