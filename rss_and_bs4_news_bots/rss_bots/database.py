import sqlite3
from rss_and_bs4_news_bots.bots_info import *

print(BASE_DIR)


def connect_and_record(source="", title="", category="", subcategory="", description="", pubDate="", link="",
                       thumbnail_url=""):
    if pubDate == "":
        pass
    vt = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    im = vt.cursor()
    # im.execute("CREATE TABLE IF NOT EXISTS isomer (id INTEGER PRIMARY KEY, isim TEXT NOT NULL UNIQUE)")
    try:
        im.execute(
            "INSERT INTO news_news( source,title,category,subcategory,description,pubDate,link,thumbnail_url) VALUES (?,?,?,?,?,?,?,?)",
            [source, title, category, subcategory, description, pubDate, link, thumbnail_url])
        print(im.lastrowid)
        print("Yeni veri eklendi : ",title)
    except:
        pass
        #print("veri mevcut kayıt edilmedi")

    last_record_id = im.lastrowid
    vt.commit()
    vt.close()
    if last_record_id:
        return last_record_id
    else :
        return -1