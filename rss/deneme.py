# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_bot.settings")
# import django
# django.setup()
#
# from news.models import source_data
#
# if __name__ == '__main__':
#     q = source_data.objects.first()
#
# from scrapinghub import ScrapinghubClient
# apikey = "cc7abc1ea51f4b109434cc9e8e0802f2"
#
# client = ScrapinghubClient(apikey)
# project_ıd_list = client.projects.list()
# project = client.get_project(project_ıd_list[0])
# for spider in project.spiders.list():
#     print(spider["id"])
#     spider_i = project.spiders.get(spider["id"])
#
#     last_job_list = list(spider_i.jobs.iter_last())
#     last_job_key = last_job_list[0]["key"]
#     job = client.get_job(last_job_key)
#     for item in job.items.iter():
#         print(item["source"])
#     print("last job of spider : ", last_job_key)

from datetime import datetime

import re

 # define desired replacements here

# use these three lines to do the replacement
# rep = dict((re.escape(k), v) for k, v in rep.items())
# #Python 3 renamed dict.iteritems to dict.items so use rep.items() for latest versions
# pattern = re.compile("|".join(rep.keys()))
# text = pattern.sub(lambda m: rep[re.escape(m.group(0))], str_date)
# print(text.replace("Mart","03",1))

def replace_all(text):
    dic = {"Ocak": "01", "Şubat": "02", "Mart": "03", "Nisan": "04", "Mayıs": "05", "Haziran": "06",
           "Temmuz": "07", "Ağustos": "08", "Eylül": "09", "Ekim": "10", "Kasım": "11", "Aralık": "12",
           "Pazartesi": "", "Salı": "", "Çarşamba": "", "Perşembe": "", "Cuma": "", "Cumartesi": "","Pazar": "",
           ",":"","  ":" ","   ":" "}
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


if __name__ == '__main__':
    str_date = "30 mart 2021 Salı, 21:53"
    print(replace_all(str_date))

    d = datetime.now()
    print(d)
    print(str(d))

# datetime.strptime(str_date,"")

#
# for item in job.items.iter():
#     # print(item)
#     pass

 #    dict = {
 #        'title': item['title'][0],
 #        'director': item['director'][0],
 #        'summary': item['summary'][0]
 #    }
 #    data.append(dict)
 #
 # TODO : Burada kaldım zyte apisini bağla
