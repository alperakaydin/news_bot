from django.contrib import admin
from django.urls import path
from .views import *




urlpatterns = [
    path('index/', indexpage),
    path('deneme/', deneme),
    path('borsa/', borsa),
    path('gundem/', gundem),
    path('yasam/', yasam),
    path('run/', run_bot_remote),
    path('index/<int:id>/',news_add_user )

]

