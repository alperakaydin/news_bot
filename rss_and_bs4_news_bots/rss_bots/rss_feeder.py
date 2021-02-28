import sqlite3

from pathlib import Path
from rss_and_bs4_news_bots.bots_info import *
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime
from time import mktime

def struct_t_to_datetime(struct):
    dt = datetime.fromtimestamp(mktime(struct))
    return dt

class haber:
    def __init__(self, title, source, description, link, date, img_src):

        self.title = title
        self.source = source
        self.description = description
        self.link = link
        self.date = date
        self.img_src = img_src

class Get_news_functions:


    def ntv_ekonomi(rss_link):
        haberlistesi=[] #Haber class listesi
        p = feedparser.parse(rss_link)
        items = p.entries
        for item in items:
            bs= BeautifulSoup(item.description, "html.parser")
            img_src = bs.find("img").get("src")
            dt = item.date_parsed
            new_date = struct_t_to_datetime(dt)
            description = bs.text

            haberclass = haber(item.title, "ntv", description, item.link, new_date, img_src)
            haberlistesi.append(haberclass)
        return haberlistesi


if __name__ == "__main__":
    #print(RSS_LİNKS["dunya-genel"])
    #ntv_ekonomi_haber_listesi = Get_news_functions.ntv_ekonomi("https://www.ntv.com.tr/dunya.rss" )

    """print(BASE_DIR)
    vt = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    for row in vt.execute('SELECT * FROM news_news'):
        print(row)

    vt.close()
"""
    print(ntv_ekonomi_haber_listesi[0].title)
    print(ntv_ekonomi_haber_listesi[0].date)
    print(ntv_ekonomi_haber_listesi[0].link)
    print(ntv_ekonomi_haber_listesi[0].description)
    print(ntv_ekonomi_haber_listesi[0].img_src)
    #print(ntv_ekonomi_haber_listesi[2].title)