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
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_bot.settings")
import django
django.setup()

from news.models import source_data , news, settings


regex = r"([a-z\×_ğüşıöçĞÜŞİÖÇ\-_0-9\/\:\.]*\.(jpg|jpeg|png|gif))"
regex_cdata = r"(<!\[CDATA\[)|(\]]>)"

#from scrapinghub import ScrapinghubClient


apikey = "cc7abc1ea51f4b109434cc9e8e0802f2"
job_id = "514165/1/1"




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
def replace_strdate(text):
    dic = {"Ocak": "01", "Şubat": "02", "Mart": "03", "Nisan": "04", "Mayıs": "05", "Haziran": "06",
           "Temmuz": "07", "Ağustos": "08", "Eylül": "09", "Ekim": "10", "Kasım": "11", "Aralık": "12",
           "Pazartesi": "", "Salı": "", "Çarşamba": "", "Perşembe": "", "Cuma": "", "Cumartesi": "","Pazar": "",
           ",":"","  ":" ","   ":" "}
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def struct_t_to_datetime(struct):
    dt = datetime.fromtimestamp(mktime(struct))
    return dt

def rss_get_news_and_record():
    sources = source_data.objects.all()
    print("sources : ", sources)
    for source_db in sources:
        source = source_db.source_name
        url = source_db.url
        category = source_db.category
        time_code = source_db.time_code
        active = source_db.active
        is_youtube = source_db.is_youtube
        # print(source_db)

        title = ""

        description = ""
        pubDate = ""
        link = ""
        thumbnail_url = ""
        try:
            if active:
                added_news_count = 0
                image_test = ""
                image_flag = True
                try:
                    res = requests.get(url, headers=HEADERS,  timeout=REQUEST_TIME_OUT ) #proxies=PROXIES,
                    # print(url, "\t Status Code: ", res.status_code)
                    # print(" 2  : ", datetime.now())
                except requests.exceptions.Timeout as e:
                    # print(url, "\t\t\tException : ", e.strerror)
                    pass

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
                    # print("news_num : ",news_num)
                    # print(" 4  : ", datetime.now())
                    for i in range(news_num):



                        ######### LİNK - FEEDPARSER #########
                        if fp_items[i].has_key("link"):
                            link= fp_items[i].link
                            # print("link : ", link)


                        #  DATABASE EXİSTS
                        if news.objects.all().filter(link=link).exists() == False:

                            ######### TİTLE - FEEDPARSER #########
                            if fp_items[i].has_key("title"):
                                # TİTLE CDATA REGEX HANDLER
                                title_re = re.sub(regex_cdata, "", fp_items[i].title, 0)
                                if title_re:
                                    title = title_re
                                else:
                                    title = fp_items[i].title




                            ######### PUBLİSHED DATE - FEEDPARSER #########
                            if fp_items[i].has_key("published"):
                                pubDate=struct_t_to_datetime(fp_items[i].published_parsed )+ timedelta(hours=int(time_code))
                            # print(" 5  : ", datetime.now())
                            try:

                                ######### DESCRİPTİON - FEEDPARSER #########
                                if fp_items[i].has_key("description"):
                                    description = fp_items[i].summary_detail.value

                                    # print("######### DESCRİPTİON - FEEDPARSER #########")

                                ######### DESCRİPTİON - BEAUTİFULSOUP #########
                                elif bs_items[i].description.text:
                                    description = bs_items[i].description.text
                                    # print("######### DESCRİPTİON - BEAUTİFULSOUP #########")
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
                            elif fp_items[i].enclosures:
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


                            #  DATABASE OPERATİONS
                            new_news = news.objects.create(source=source, title=title, category=category,
                                                           description=description, pubDate=pubDate,
                                                           link=link, thumbnail_url=thumbnail_url)
                            new_news.save()
                            added_news_count +=1
                            #######################


                        else:
                            # print("*******veri mevcut********")
                            pass
                print("Status Code :  ", res.status_code,"\t Added News Count : ",added_news_count,  "\t", url)


            else:
                pass
        except:
            pass


#def scrapy_get_cloud_and_record():
    #
    # client = ScrapinghubClient(apikey)
    # project_id_list = client.projects.list()
    # project = client.get_project(project_id_list[0])
    #
    # for spider in project.spiders.list():
    #     print(spider["id"])
    #     spider_i = project.spiders.get(spider["id"])
    #
    #     last_job_list = list(spider_i.jobs.iter_last())
    #     last_job_key = last_job_list[0]["key"]
    #     job = client.get_job(last_job_key)
    #
    #
    #     added_news_count=0
    #     for item in job.items.iter():
    #
    #         source = item["source"]
    #         link = item["link"]
    #         if news.objects.all().filter(link=link).exists() == False:
    #
    #
    #             title = item["title"]
    #             category = item["category"]
    #             description = item["description"]
    #             pubDate = item["pubDate"]
    #             thumbnail_url = item["thumbnail_url"]
    #             is_company_news = None
    #             company_code = None
    #
    #             if "is_company_news" in item:
    #                 if item["is_company_news"] == True:
    #                     is_company_news = True
    #                     company_code = item["company_code"]
    #
    #             new_news = news.objects.create(source=source, title=title, category=category,
    #                                            description=description, pubDate=pubDate,
    #                                            link=link, thumbnail_url=thumbnail_url,
    #                                            company_code=company_code, is_company_news=is_company_news)
    #             new_news.save()
    #             added_news_count+=1
    #
    #     print("Job Key  :  ", job.key, "\t Added News Count : ", added_news_count )
    #

def run_rss_schedular():
    print("\n")
    print("RSS started..")
    now = datetime.now()
    rss_get_news_and_record()
    excecution_time = datetime.now() - now
    print("ExcecutionTime  :  ",excecution_time)
    print("###  ---  RSS Finished..")


def run_scrapy_functions():
    print("\n")
    print("SCRAPY started..")
    now = datetime.now()
    scrapy_get_cloud_and_record()
    excecution_time = datetime.now() - now
    print("ExcecutionTime  :  ", excecution_time)
    print("###  ---  SCRAPY Finished..")

if __name__ == '__main__':
    run_rss_schedular()
    run_scrapy_functions()
    sleep(120)
    print("\n")
    print(" -----     Program is sleeping     -----")
