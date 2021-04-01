from builtins import id

from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_http_methods


from news.models import news, company_news ,video_source ,source_data
from datetime import datetime ,timedelta ,date
from django.http import JsonResponse
from django.contrib.auth.models import User , Group
import django.utils.timezone
from django.utils.timesince import timesince
import json
import time

from rss.rss3 import rss_get_news_and_record

"""
   
"""

####  MY HELPER FUNCTİONS
def getToday():
    return date.today().day

#### NEWS Parse Function
def parse(request):
    rss_get_news_and_record()
    return HttpResponse("parse edildi")


def getShareCount (r):
    shareCount = r.user.selected_news.all().filter(is_admin=True).filter(
        pubDate__day=getToday()).count()
    return shareCount

def createContent(request , viewName , queryList):
    if request.user.is_authenticated:

        queryset = news.objects.filter(category__in=queryList).filter(is_admin=False).filter(is_editor=False).filter(  # Burası
            pubDate__day=getToday()).order_by(
            '-pubDate')
        haber_sayisi = len(queryset)
        content={}
        if request.user.groups.filter(name="editors").exists():

            content = {
                "haberler": queryset,
                "haber_sayisi": haber_sayisi,
                "username": request.user.username,
                "page": viewName,  # ----------
                "is_yonetici": False,
                "shareCount": getShareCount(request)
            }
        elif request.user.groups.filter(name="yonetici").exists():

            users_in_group = Group.objects.get(name="editors").user_set.all()

            content = {
                "haberler": queryset,
                "haber_sayisi": haber_sayisi,
                "username": request.user.username,
                "page": viewName,  # ----------
                "is_yonetici": True,
                "users_in_group": users_in_group,
                "shareCount": getShareCount(request)
            }

        return render(request=request, template_name="../templates/news/index.html", context=content)
    else:
        return redirect("/login/")

####  MY HELPER FUNCTİONS


###  APİ FUNCTİONS
def dataAPIView(request):


    special_time = datetime.now() - timedelta(days=1)
    borsaCount = request.user.selected_news.all().filter(pubDate__day=getToday()).filter(
        category__in=["borsa"]).filter(is_editor=True).count()
    gundemCount = request.user.selected_news.all().filter(is_editor=True).filter(pubDate__day=getToday()).filter(
        category__in=["gundem"]).count()
    yasamCount = request.user.selected_news.all().filter(is_editor=True).filter(pubDate__day=getToday()).filter(
        category = "yasam" ).count()
    sporCount = request.user.selected_news.all().filter(is_editor=True).filter(pubDate__day=getToday()).filter(
        category = "spor" ).count()
    otomobilCount = request.user.selected_news.all().filter(is_editor=True).filter(pubDate__day=getToday()).filter(
        category = "otomobil" ).count()
    teknolojiCount = request.user.selected_news.all().filter(is_editor=True).filter(pubDate__day=getToday()).filter(
        category="teknoloji").count()
    shareCount = request.user.selected_news.all().filter(is_admin=True).filter(pubDate__day=getToday()).count()
    print(request.user.username, " : ", shareCount, " teknoloji : ", teknolojiCount)
    return JsonResponse({
                "User": request.user.username,
                "error":False,
                "borsaCount":borsaCount,
                "gundemCount":gundemCount,
                "yasamCount":yasamCount,
                "sporCount":sporCount,
                "otomobilCount":otomobilCount,
                "teknolojiCount":teknolojiCount,
                "shareCount":shareCount,
                "selectedCount":borsaCount+gundemCount+yasamCount+sporCount,
                "notification":True,
                "notificationMessage":"HaberTitle burası dict olacak"
            })

def dashboardDataAPIView(request):
    special_time = datetime.now() - timedelta(days=1)

    users =  Group.objects.get(name="editors").user_set.all()
    today_data  = []

    for user in users:
        attr = dict()
        item = {"username": user.username}
        attr["username"] = user.username
        attr["news_count"] = user.selected_news.all().filter(is_admin=True).filter(pubDate__gte=special_time).count()
        attr["last_login"] = str(timesince(user.last_login))+" önce"
        # print(datetime.ctime(datetime.now() - user.last_login))
        today_data.append(attr)

    print(today_data)

    this_week = datetime.now() - timedelta(weeks=1)

    week_data = []

    for user in users:
        attr = dict()
        item = {"username": user.username}
        attr["username"] = user.username
        week_count = user.selected_news.all().filter(is_admin=True).filter(pubDate__gte=this_week).count()
        attr["news_count"] = week_count
        attr["daily_avarage"] = int((week_count/7)+0.5)
        # print(datetime.ctime(datetime.now() - user.last_login))
        week_data.append(attr)

    print(week_data)




    today_news_count = news.objects.all().filter(is_admin=True).filter(pubDate__gte=special_time).count()
    today_economie_count = news.objects.all().filter(is_admin=True).filter(category__in=["borsa","gundem","ekonomi"]). filter(pubDate__gte=special_time).count()
    today_stil_count = news.objects.all().filter(is_admin=True).filter(category__in=["yasam","spor","teknoloji","otomobil"]). filter(pubDate__gte=special_time).count()
    today_total_news = news.objects.all().filter(pubDate__gte=special_time).count()
    total_source_number = source_data.objects.all().count()
    return JsonResponse({
        "today_news_count":today_news_count,
        "today_economie_count":today_economie_count,
        "today_stil_count":today_stil_count,
        "today_total_news":today_total_news,
        "total_source_number":total_source_number,
        "users_data":today_data,
        "users_weekly_data":week_data,
    })


def news_add_userAPI(request, id):
    # editorler = User.groups.all()# objects.filter(groups__in='editors')
    # print(editorler.model.username)
    # if request.user.groups.filter(name = "editors").exists():
    #     print(request.user.groups.all())
    #     users_in_group = Group.objects.get(name="editors").user_set.all()
    #     for us in users_in_group:
    #         print(us.username)


    if request.user.is_authenticated:
        username = request.user.username
        print(request.user.username ,"  den bu id li haber",id)
        haber = news.objects.get(id=id)
        user = User.objects.get(username=username)

        if request.user.groups.filter(name = "editors").exists():

            if haber.is_admin == True:
                return JsonResponse({
                    "message": "Bu haber sizinle paylaşıldı",
                    "error": True
                })
            ### Validator
            now = datetime.now()
            special_time = now - timedelta(days=1)
            same_source = news.objects.filter(source=haber.source).filter(user=user).filter(
                pubDate__gte=special_time).count()

            permission_count = source_data.objects.filter(
                source_name=haber.source).first().permission_count  ### İZİN VERİLEN HABER SAYISI
            if same_source >= permission_count:
                return JsonResponse({
                    "message": "Bu kaynak için sınıra ulaştınız..",
                    "error": True
                })
            else:
                haber.user.add(user)
                haber.is_editor = True
                haber.save()
                message = f"Haber eklendi İD: {id} "

                user_select_count = user.selected_news.all().filter(pubDate__gte=special_time).filter(
                    category__in=["analiz", "ekonomi"]).count()

                print(same_source)
                return JsonResponse({
                    "message": message,
                    "source": haber.source,
                    "count": same_source + 1,
                    "error": False,
                    "category": "borsa",
                    "categoryCount": user_select_count
                })
        # if request.user.groups.get().name == 'yonetici':
        # else:
        #     ### Validator
        #     now = datetime.now()
        #     special_time = now - timedelta(days=1)
        #     same_source = news.objects.filter(source=haber.source).filter(user=user).filter(
        #         pubDate__gte=special_time).count()
        #     if same_source >= 3:
        #         return JsonResponse({
        #             "message": "Bu kaynak için sınıra ulaştınız..",
        #             "error":True
        #         })
        #     else :
        #         haber.user.add(user)
        #         haber.is_editor = True
        #         haber.save()
        #         message = f"Haber eklendi İD: {id} "
        #
        #         user_select_count = user.selected_news.all().filter(pubDate__gte=special_time).filter(category__in=["analiz", "ekonomi"]).count()
        #
        #         print(same_source)
        #         return JsonResponse({
        #             "message":message,
        #             "source":haber.source,
        #             "count":same_source+1,
        #             "error": False,
        #             "category":"borsa",
        #             "categoryCount":user_select_count
        #         })

    else:
        return JsonResponse({"message": "Lütfen giriş yapınız"})

def news_delete_userAPI(request, id):
    if request.user.is_authenticated:
        username = request.user.username
        print(request.user.username ,"  den bu id li haber",id)
        haber = news.objects.get(id=id)
        user = User.objects.get(username=username)
        haber.user.remove(user)
        haber.is_editor = False
        haber.save()
        message = f"Haber silindi İD: {id} "

        now = datetime.now()
        special_time = now - timedelta(days=1)
        same_source = news.objects.filter(source=haber.source).filter(user=user).filter(
            pubDate__gte=special_time).count()

        return JsonResponse({
            "message":message,
            "source": haber.source,
            "count": same_source
        })
#
    else:
        return JsonResponse({"message": "Lütfen giriş yapınız"})

def news_add_yoneticiAPI(request, username, id ):
    if request.user.groups.filter(name = "yonetici").exists():
        now = datetime.now()
        special_time = now - timedelta(days=1)

        editor = User.objects.get(username=username)
        haber = news.objects.get(id=id)
        haberSource = haber.source

        if editor.selected_news.all().filter(id=id).exists(): # Editör zaten haberi seçmişse
            return JsonResponse({
                "message": f"Bu haber {editor.username} tarafından zaten eklenmiş..",
                "error": True
            })


        same_source = news.objects.filter(source=haberSource).filter(user=editor).filter(
            pubDate__gte=special_time).count()

        permission_count = source_data.objects.filter(source_name=haberSource).first().permission_count ### İZİN VERİLEN HABER SAYISI

        if same_source >= permission_count :
            return JsonResponse({
                "message": "Bu kaynak için sınıra ulaştınız..",
                "error": True
            })

        haber.user.add(editor)
        haber.is_admin = True
        haber.save()

        return JsonResponse({
            "message": "Haber başarıyla gönderildi..",
            "error": False
        })

###  APİ FUNCTİONS

###   VİDEO VİEW

# @require_http_methods(['GET','POST'])
def video_view(request, category):

    if request.user.is_authenticated:
        if category == "borsa":
            queryset =  video_source.objects.get(category="borsa")
        elif category == "yasam":
            queryset =  video_source.objects.get(category="yasam")
        elif category == "spor":
            queryset =  video_source.objects.get(category="spor")
        elif category == "teknoloji":
            queryset =  video_source.objects.get(category="teknoloji")
        elif category == 'otomobil':
            queryset =  video_source.objects.get(category="otomobil")

        if request.user.groups.filter(name="yonetici").exists():
            is_yonetici = True
        elif request.user.groups.filter(name="editor").exists():
            is_yonetici = False
        else:
            is_yonetici = False
        content = {
            "username": request.user.username,
            "page": "video",
            "queryset":queryset,
            "shareCount": getShareCount(request),
            "is_yonetici":is_yonetici
        }
    else:
        content = {

            "username": "Misafir",
            "page": "sirket_haber"
        }
    return render(request=request, template_name="../templates/news/video/video-template.html", context=content)
###   VİDEO VİEW


###  ÖZEL VİEWLER
def selected(request):
    username = request.user.username
    editor = User.objects.get(username=username)

    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = editor.selected_news.all().filter(pubDate__day=getToday()).filter(is_admin=False).order_by('-pubDate')

    haber_sayisi = len(queryset)


    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username,
            "selected":True,
            "shareCount": getShareCount(request)
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir",
            "selected": False,
            "shareCount": getShareCount(request)
        }
    return render(request=request, template_name="../templates/news/index.html", context=content)

def share(request):
    username = request.user.username
    editor = User.objects.get(username=username)

    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = editor.selected_news.all().filter(pubDate__day=getToday()).filter(is_admin=True).order_by('-pubDate')

    haber_sayisi = len(queryset)


    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username,
            "selected":True,
            "shareCount": getShareCount(request)
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir",
            "selected": False,
            "shareCount": getShareCount(request)
        }
    return render(request=request, template_name="../templates/news/index.html", context=content)

###  ÖZEL VİEWLER


###  DEFAULT VİEWS
def borsa(request):
    return createContent(request, "borsa", ["borsa","ekonomi", "analiz"])

def gundem(request):
    return createContent(request, "gundem", ["gundem"])

def teknoloji(request):
    return createContent(request, "teknoloji", ["teknoloji"])

def yasam(request):
    return createContent(request, "yasam", ["yasam"])

def spor(request):
    return createContent(request, "spor", ["spor"])

def otomobil(request):
    return createContent(request, "otomobil", ["otomobil"])

def sirket_haber_view(request):
    return createContent(request, "sirket", ["sirket"])

###  DEFAULT VİEWS


###  KONTROL VE SİL
@require_http_methods(['GET','POST'])
def indexpage(request):

    queryset = news.objects.filter(category__in=["yasam", "ekonomi"]).filter(pubDate__day=getToday()).filter(is_admin=False).order_by('-pubDate')

    #queryset = news.objects.filter(pubDate__gte=special_time ).order_by('-pubDate')
    haber_sayisi = len(queryset)
    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username,
            "page":"index"
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir",
            "page": "index"
        }
    return render(request=request, template_name="../templates/news/index.html", context=content)

# def sirket_haber_view(request):
#     today = datetime.today()
#     queryset = company_news.objects.all()
#     print(len(queryset))
#
#     if request.user.is_authenticated:
#         content = {
#             "haberler": queryset,
#
#             "username": request.user.username,
#             "page": "sirket_haber"
#         }
#     else:
#         content = {
#             "haberler": queryset,
#             "username": "Misafir",
#             "page": "sirket_haber"
#         }
#     return render(request=request, template_name="../templates/news/sirkethaber.html", context=content)

###  KONTROL VE SİL
