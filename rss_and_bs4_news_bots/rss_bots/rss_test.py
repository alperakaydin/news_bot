import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime
from rss_and_bs4_news_bots.bots_info import *
import requests
from rss_and_bs4_news_bots.rss_bots.database import *


def struct_t_to_datetime(struct):
    dt = datetime.fromtimestamp(mktime(struct))
    return dt

def rss_get_news_and_record(item):
    url=item["rss"]
    category=item["category"]
    subcategory = item["subcategory"]
    source = ""
    title = ""

    description = ""
    pubDate = ""
    link = ""
    thumbnail_url = ""
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}
    try:
        res = requests.get(url,headers=headers)
        print(url, "\t Status Code: ", res.status_code)


        fp = feedparser.parse(url_file_stream_or_string=res.content)

        bs = BeautifulSoup(res.content, features="xml", from_encoding='UTF-8')

        bs_items = bs.findAll("item")
        fp_items = fp["entries"]
        news_source = fp.feed.title
        news_num = len(fp_items)
        for i in range(news_num):

            # Feedparser
            # TİTLE

            if fp_items[i].title:
                #print(fp_items[i].title)
                title = fp_items[i].title

            if fp_items[i].link:
                #print(fp_items[i].link)
                link= fp_items[i].link

            if fp_items[i].published:
                #print(fp_items[i].published_parsed)
                pubDate=struct_t_to_datetime(fp_items[i].published_parsed)

            if fp_items[i].description:
                description = fp_items[i].summary_detail.value
                #print("feed",description)
            if bs_items[i].description.text:
                description = bs_items[i].description.text
                #print("Beautiful",description)


            # IMAGE CAPTURE
            if fp_items[i].enclosures:
                #print(type(fp_items[i].enclosures[0].href))
                #print("feedparseden resim alındı", fp_items[i].enclosures[0].href)
                thumbnail_url=fp_items[i].enclosures[0].href


            else:
                # BeautifulSoup
                if bs_items[i].image:
                    if bs_items[i].image.url:
                        #print("image 2.dereceden bulundu", bs_items[i].image.url.text)
                        thumbnail_url=bs_items[i].image.url.text

                    else:
                        if bs_items[i].image.text:
                            #print("image 1.dereceden bulundu", bs_items[i].image.text)
                            thumbnail_url= bs_items[i].image.text

                if item["no-image"]:
                    thumbnail_url = item["no-image"]

            connect_and_record(source=source,title=title,category=category,
                               subcategory=subcategory,description=description,pubDate=pubDate
                               ,link=link,thumbnail_url=thumbnail_url)

    except:
        print("error with : ",url )

if __name__ == "__main__":
    rss_get_news_and_record(RSS_LİNKS["haberturk-gundem"])
    #RSS_LİNKS["dunya-genel"]