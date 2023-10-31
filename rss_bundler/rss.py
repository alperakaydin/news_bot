import feedparser
from bs4 import BeautifulSoup
from datetime import datetime,timedelta
from time import mktime ,time,sleep
import requests
import sqlite3
import json
import os
from pathlib import Path
import re

regex = r"([a-z\×_ğüşıöçĞÜŞİÖÇ\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif))"

def get_base_dır():

    return Path(__file__).resolve().parent

# -------------------------------------------------------------
# Requests settings :
REQUEST_TIME_OUT = 6
PROXIES = {'https': 'http://fAg56g:fAg56g@91.241.49.14:3457/'}
HEADERS = {'User-Agent': 'Mozilla/5.0 '}

# Running Frequency(seconds) :
FREQUENCY = 120

# Path Variables
PATH_DATA_JSON = os.path.join(get_base_dır(), 'data.json') # Same directory
PATH_DB = Path(__file__).resolve().parent.parent / 'db.sqlite3' # Manage.py level

# Data.json settings
# Regex ifade kullanmak için data.json da special_field a sayı atamak gerek. ve kütüphanelerin altındaki regexi de dinamik yap  !

# special code 1 : descriptionda cdata olmayan ve image içeren Ör: borsatek-ekonomi
# special code 2 : descriptionda cdata verisi içerisinden image varsa  Ör: ntvspor-basketbol
# -------------------------------------------------------------




def connect_and_record(source="", title="", category="", subcategory="", description="", pubDate="", link="",
                       thumbnail_url=""):
    if pubDate == "":
        pass
    vt = sqlite3.connect(PATH_DB)
    im = vt.cursor()
    # im.execute("CREATE TABLE IF NOT EXISTS isomer (id INTEGER PRIMARY KEY, isim TEXT NOT NULL UNIQUE)")
    try:
        im.execute(
            "INSERT INTO news_news( source,title,category,subcategory,description,pubDate,link,thumbnail_url,is_favorite,is_admin) VALUES (?,?,?,?,?,?,?,?,?,?)",
            [source, title, category, subcategory, description, pubDate, link, thumbnail_url,False,False])
        print(im.lastrowid)
        print("Yeni veri eklendi : ",title)
    except Exception:

        print(Exception )

    last_record_id = im.lastrowid
    vt.commit()
    vt.close()
    if last_record_id:
        return last_record_id
    else :
        return -1

def connect_and_get_data():
    vt = sqlite3.connect(PATH_DB)
    im = vt.cursor()
    # im.execute("CREATE TABLE IF NOT EXISTS isomer (id INTEGER PRIMARY KEY, isim TEXT NOT NULL UNIQUE)")

    im.execute("SELECT * from news_source_data")
    data = im.fetchall()


    vt.close()
    return data


def struct_t_to_datetime(struct):
    dt = datetime.fromtimestamp(mktime(struct))
    return dt

def rss_get_news_and_record(item):

    url=item["rss"]
    category=item["category"]
    subcategory = item["subcategory"]
    #src = item["name"].split()
    source = item["name"]
    title = ""
    time_code=item["time_code"]
    description = ""
    pubDate = ""
    link = ""
    thumbnail_url = ""
    special_code = item["field_code"]
    print("4")
    try:
        res = requests.get(url, headers=HEADERS,  timeout=REQUEST_TIME_OUT ) #proxies=PROXIES,
        #print(url, "\t Status Code: ", res.status_code)

        # print("1")
        fp = feedparser.parse(url_file_stream_or_string=res.content)
        # print("2")
        bs = BeautifulSoup(res.content, features="xml", from_encoding='UTF-8')
        # print("3")
        bs_items = bs.findAll("item")
        fp_items = fp["entries"]
        # news_source = fp.feed.title
        news_num = len(fp_items)
        # print("4")
        for i in range(news_num):
            print("5")
            # Feedparser
            # TİTLE

            if fp_items[i].title:
                print(fp_items[i].title)
                title = fp_items[i].title
                # print("5")
            if fp_items[i].link:
                #print(fp_items[i].link)
                link= fp_items[i].link
                # print("6")
            if fp_items[i].published:
                #print(fp_items[i].published_parsed)
                pubDate=struct_t_to_datetime(fp_items[i].published_parsed )+ timedelta(hours=time_code)
                # print("7")
            try:
                if fp_items[i].description:
                    description = fp_items[i].summary_detail.value
                    # print("8")
                elif bs_items[i].description.text:
                    description = bs_items[i].description.text
                    #print("Beautiful",description)
                    # print("9")
            except:
                pass

            # IMAGE CAPTURE
            if fp_items[i].has_key('media_content'):
                thumbnail_url = fp_items[i].media_content[0]["url"]
            if fp_items[i].enclosures:
                #print(type(fp_items[i].enclosures[0].href))
                #print("feedparseden resim alındı", fp_items[i].enclosures[0].href)
                thumbnail_url=fp_items[i].enclosures[0].href
                # print("10")


            else:
                # print("11")
                # BeautifulSoup
                try:
                    if bs_items[i].image:
                        # print("12")
                        if bs_items[i].image.url:
                            # print("13")
                            #print("image 2.dereceden bulundu", bs_items[i].image.url.text)
                            thumbnail_url=bs_items[i].image.url.text

                        else:
                            if bs_items[i].image.text:
                                # print("14")
                                #print("image 1.dereceden bulundu", bs_items[i].image.text)
                                thumbnail_url= bs_items[i].image.text
                                # print("14,1")
                except:
                    pass
            if special_code == 1:
                try:
                    matches = re.search(regex, description, re.IGNORECASE)

                    thumbnail_url=matches.group()
                except:
                    print("picture not found")

            if special_code == 2:
                try:
                    listToStr = ' '.join(map(str, fp_items[i].content))
                    matches = re.search(regex,listToStr , re.IGNORECASE)

                    thumbnail_url=matches.group()
                except:
                    print("picture not found")


            connect_and_record(source=source,title=title,category=category,
                               subcategory=subcategory,description=description,pubDate=pubDate
                               ,link=link,thumbnail_url=thumbnail_url)
        print("6")
    except requests.exceptions.RequestException as e:
        print(e)

def run_rss_schedular():

    rss_data = json.load(open(PATH_DATA_JSON , "r", encoding="utf-8"))
    for item in rss_data:
        print("hhhhhsssh")
        print(type(item))
        print(item["name"],"   Kaynağından haberler alınıyor")
        print("2")
        rss_get_news_and_record(item)
        print("3")
        print("------%100--------")

def run_bot():
    run_rss_schedular()
    print("Program UYUYOR :) ")
    sleep(FREQUENCY)
if __name__ == '__main__':

    while True:
        print("hhhhhh")
        #schedule.every(2).minutes.do(run_rss_schedular())
        run_bot()
    # print(connect_and_get_data())