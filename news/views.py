from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_http_methods
from news.models import news
from rss_and_bs4_news_bots.rss_bots.rss_feeder import *
from datetime import datetime ,timedelta
from django.http import JsonResponse
from django.contrib.auth.models import User
from rss_and_bs4_news_bots.run_bot import *
import time
"""
    Zaman problemi mi date kavramını öğren hangi tipte çalışacağına karar ver veritabanındaki tipe bak
    
"""

@require_http_methods(['GET','POST'])
def indexpage(request):
    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = news.objects.filter(category__in=["yasam", "ekonomi"]).filter(pubDate__gte=special_time ).order_by('-pubDate')

    #queryset = news.objects.filter(pubDate__gte=special_time ).order_by('-pubDate')
    haber_sayisi = len(queryset)
    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir"
        }
    return render(request=request, template_name="index.html", context=content)

def deneme(request):
    e = Get_news_functions.ntv_ekonomi("https://www.ntv.com.tr/dunya.rss")
    for i in range(len(e)):
        q = news(title=e[i].title, source="src", description=e[i].description, link=e[i].link, pubDate= e[i].date ,
                 thumbnail_url=e[i].img_src)
        q.save()

    return redirect("/news/index")

def news_add_user(request, id):
    if request.user.is_authenticated:
        username = request.user.username
        print(request.user.username ,"  den bu id li haber",id)
        haber = news.objects.get(id=id)
        user = User.objects.get(username=username)
        haber.user.add(user)
        message = f"Haber eklendi İD: {id} "


        return JsonResponse({"message":message})

    else:
        return JsonResponse({"message": "Lütfen giriş yapınız"})

def borsa(request):
    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = news.objects.filter(category__in=["analiz", "ekonomi"]).filter(pubDate__gte=special_time).order_by(
        '-pubDate')

    haber_sayisi = len(queryset)

    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir"
        }
    return render(request=request, template_name="index.html", context=content)

def gundem(request):
    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = news.objects.filter(category__in=["gundem", "genel","dunya","turkiye"]).filter(pubDate__gte=special_time).order_by(
        '-pubDate')

    haber_sayisi = len(queryset)

    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir"
        }
    return render(request=request, template_name="index.html", context=content)

def yasam(request):
    now = datetime.now()
    special_time = now - timedelta(days=2)
    queryset = news.objects.filter(category__in=["yasam"]).filter(pubDate__gte=special_time).order_by(
        '-pubDate')

    haber_sayisi = len(queryset)

    if request.user.is_authenticated:
        content = {
            "haberler": queryset,
            "haber_sayisi" : haber_sayisi,
            "username": request.user.username
        }
    else:
        content = {
            "haberler": queryset,
            "haber_sayisi": haber_sayisi,
            "username": "Misafir"
        }
    return render(request=request, template_name="index.html", context=content)

def run_bot_remote(request):
    if request.user.is_authenticated:
        run_rss_schedular()
        return JsonResponse({"message":"bot çalıştı"})

    else:
        return JsonResponse({"message": "Lütfen giriş yapınız"})