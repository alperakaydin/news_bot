from rss_and_bs4_news_bots.rss_bots.rss_test import *
import json
import os
def run_rss_schedular():
    path = os.path.join(os.path.join(BASE_DIR ,'rss_and_bs4_news_bots'),'data.json')
    rss_data = json.load(open(path , "r", encoding="utf-8"))
    for item in rss_data:
        print(type(item))
        print(item["name"],"   Kaynağından haberler alınıyor")

        rss_get_news_and_record(item)
        print("------%100--------")

#schedule.every(2).minutes.do(run_rss_schedular())
#if __name__ == "__main__":
    #run_rss_schedular(1,1)

"""while True:
    run_rss_schedular()
    print("Program UYUYOR :) ")
    time.sleep(120)
"""
if __name__ == "__main__":
    path = os.path.join(os.path.join(BASE_DIR ,'rss_and_bs4_news_bots'),'data.json')
    print(path)
    rss_data = json.load(open(path, "r", encoding="utf-8"))
    print(rss_data)