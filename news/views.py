from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_http_methods
from news.models import news
from rss_and_bs4_news_bots.rss_bots.rss_feeder import *
import datetime
"""
    Zaman problemi mi date kavramını öğren hangi tipte çalışacağına karar ver veritabanındaki tipe bak
    
"""
@require_http_methods(['GET','POST'])
def indexpage(request):
    now = datetime.datetime.now()
    special_time = now - datetime.timedelta(days=2)

    queryset = news.objects.filter(pubDate__gte=special_time ).order_by('-pubDate')
    haber_sayisi = len(queryset)
    content = {
        "haberler": queryset,
        "haber_sayisi" : haber_sayisi,
    }
    return render(request=request, template_name="index.html", context=content)

def deneme(request):
    e = Get_news_functions.ntv_ekonomi("https://www.ntv.com.tr/dunya.rss")
    for i in range(len(e)):
        q = news(title=e[i].title, source="src", description=e[i].description, link=e[i].link, pubDate= e[i].date ,
                 thumbnail_url=e[i].img_src)
        q.save()

    return redirect("/news/index")
"""self.title = title
        self.source = source
        self.description = description
        self.link = link
        self.date = date
        self.img_src = img_src"""
""" source = models.CharField(max_length=200, verbose_name="Kaynak", blank="")
    title = models.CharField(max_length=200, verbose_name="Başlık")
    category = models.CharField(max_length=200, verbose_name="Kategori", blank="" )
    subcategory = models.CharField(max_length=200, verbose_name="Alt Kategori", blank="")
    description = models.TextField( verbose_name="Özet", blank="")
    pubDate = models.DateTimeField( verbose_name="Yayınlanma Tarihi", blank="")
    link = models.URLField( verbose_name="Haber Link", blank="")
    thumbnail_url = models.URLField( verbose_name="Resim Link", blank="")
    is_favorite = models.BooleanField(blank=False, verbose_name="Favori")
    is_select = models.BooleanField(blank=False, verbose_name="Seç")
"""