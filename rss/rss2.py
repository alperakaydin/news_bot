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




def connect_and_record(source="", title="", category="", description="", pubDate="", link="",
                       thumbnail_url=""):
    if pubDate == "":
        pass
    vt = sqlite3.connect(PATH_DB)
    im = vt.cursor()
    # im.execute("CREATE TABLE IF NOT EXISTS isomer (id INTEGER PRIMARY KEY, isim TEXT NOT NULL UNIQUE)")
    try:
        im.execute(
            "INSERT INTO news_news( source,title,category,description,pubDate,link,thumbnail_url,is_editor,is_admin,is_video) VALUES (?,?,?,?,?,?,?,?,?,?)",
            [source, title, category, description, pubDate, link, thumbnail_url ,False,False,False])
        print(im.lastrowid)
        print("*****Yeni veri eklendi****** : ",title)
    except  Exception:
        print(Exception)
        print("#######veri mevcut kayıt edilmedi#########")

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
    print(data)

    vt.close()
    return data


def struct_t_to_datetime(struct):
    dt = datetime.fromtimestamp(mktime(struct))
    return dt

def rss_get_news_and_record(item):
    print("1 : " , item[1] ,"2 : " , item[2] ,"3 : " , item[3] ,"4 : " , item[4] ,"5 : " , item[5] ,"6 : " , item[6] ,"7 : " , item[7] ,)
    source = item[1]
    url=item[2]
    category =item[3]
    time_code = item[4]
    active = item[5]
    is_youtube = item[6]

    print(" 1  : " ,datetime.now())


    title = ""

    description = ""
    pubDate = ""
    link = ""
    thumbnail_url = ""
    try:
        if active:

            image_test = ""
            image_flag = True
            try:
                res = requests.get(url, headers=HEADERS,  timeout=REQUEST_TIME_OUT ) #proxies=PROXIES,
                print(url, "\t Status Code: ", res.status_code)
                print(" 2  : ", datetime.now())
            except requests.exceptions.Timeout as e:
                print("Exception : ", e.strerror)


            if res.status_code ==200:

                fp = feedparser.parse(url_file_stream_or_string=res.content)
                bs = BeautifulSoup(res.content, features="xml", from_encoding='UTF-8')
                # print(" 3  : ", datetime.now())
                if bs.findAll("item"):
                    bs_items = bs.findAll("item")
                elif bs.findAll("entry"):
                    bs_items = bs.findAll("entry")

                fp_items = fp["entries"]
                news_source = fp.feed.title
                news_num = len(fp_items)
                # print(" 4  : ", datetime.now())
                for i in range(news_num):
                    # Feedparser
                    # TİTLE

                    ######### TİTLE - FEEDPARSER #########
                    if fp_items[i].has_key("title"):
                        title = fp_items[i].title

                    ######### LİNK - FEEDPARSER #########
                    if fp_items[i].has_key("link"):
                        link= fp_items[i].link

                    ######### PUBLİSHED DATE - FEEDPARSER #########
                    if fp_items[i].has_key("published"):
                        pubDate=struct_t_to_datetime(fp_items[i].published_parsed )+ timedelta(hours=int(time_code))
                    # print(" 5  : ", datetime.now())
                    try:

                        ######### DESCRİPTİON - FEEDPARSER #########
                        if fp_items[i].has_key("description"):
                            description = fp_items[i].summary_detail.value

                        ######### DESCRİPTİON - BEAUTİFULSOUP #########
                        elif bs_items[i].description.text:
                            description = bs_items[i].description.text
                        # print(" 6  : ", datetime.now())
                    except:
                        description=""


                    ######### IMAGE CAPTURE - FEEDPARSER #########

                    ######### media_content - FEEDPARSER #########
                    if fp_items[i].has_key('media_content'):
                        # print("lan")
                        thumbnail_url = fp_items[i].media_content[0]["url"]
                        # image_test = "media_content - FEEDPARSER"
                        image_flag=False
                    ######### enclosures - FEEDPARSER #########
                    if fp_items[i].enclosures:
                        thumbnail_url = fp_items[i].enclosures[0].href
                        image_test = "enclosures - FEEDPARSER"
                        image_flag = False

                    ######### IMAGE CAPTURE - BEAUTİFULSOUP #########

                    else:
                        # print(" 7  : ", datetime.now())
                        try:
                            if  None  != bs_items[i].image:
                                if  None  != bs_items[i].image.url:
                                    # print("image 2.dereceden bulundu", bs_items[i].image.url.text)
                                    thumbnail_url=bs_items[i].image.url.text
                                    image_test = "image 2.dereceden bulundu"
                                    image_flag = False
                                else:
                                    if  None  != bs_items[i].image.text:
                                        # print("image 1.dereceden bulundu", bs_items[i].image.text)
                                        thumbnail_url= bs_items[i].image.text
                                        image_test = "image 1.dereceden bulundu"
                                        image_flag = False
                        except:
                            pass
                    # if special_code == 1:
                    # print(" 8  : ", datetime.now())
                    if thumbnail_url == "":
                        try:
                            matches = re.search(regex, description, re.IGNORECASE)

                            thumbnail_url=matches.group()
                            image_test = "regex"
                            image_flag = False

                        except:
                            thumbnail_url == ""
                            # print("picture not found")
                    # print(" 9  : ", datetime.now())
                    # if special_code == 2:
                    if thumbnail_url == "":
                        try:
                            listToStr = ' '.join(map(str, fp_items[i].content))
                            matches = re.search(regex,listToStr , re.IGNORECASE)

                            thumbnail_url=matches.group()
                            image_test ="regex 2 "
                            image_flag = False
                        except:
                            pass
                            # print("picture not found")
                    # print(" 10  : ", datetime.now())
                    # print(image_test ,"   :  ", thumbnail_url)
                    connect_and_record(source=source,title=title,category=category,
                                       description=description,pubDate=pubDate
                                       ,link=link,thumbnail_url=thumbnail_url)
                    # print(" 11  : ", datetime.now())
        else:
            pass
    except:
        pass
def run_rss_schedular():
    data = connect_and_get_data()
    for item in data:
        rss_get_news_and_record(item)
        print("------%100--------")

def run_bot():
    run_rss_schedular()
    print("Program UYUYOR :) ")
    sleep(FREQUENCY)



if __name__ == '__main__':

    while True:
        #schedule.every(2).minutes.do(run_rss_schedular())
        run_bot()
    # print(connect_and_get_data())
    # run_rss_schedular()