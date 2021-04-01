from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('index/', indexpage,),
    path('borsa/', borsa),
    path('gundem/', gundem),
    path('yasam/', yasam),
    path('teknoloji/', teknoloji),
    path('parse/', parse),
    path('spor/', spor),
    path('otomobil/', otomobil),
    path('sirkethaber/', sirket_haber_view),
    path('video&<str:category>/',  video_view),
    path('selected/', selected),
    path('share/', share),
    path('api/add<int:id>/', news_add_userAPI ),
    path('api/data/', dataAPIView ),
    path('api/dashboarddata/', dashboardDataAPIView ),
    path('api/delete<int:id>/', news_delete_userAPI ),
    path('api/yoneticiadd&<int:id>&<str:username>/', news_add_yoneticiAPI )

]

