# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from news.models import news, company_news
from django.db.models import Q
from datetime import datetime, timedelta
@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    special_time = datetime.now() - timedelta(days=1)
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    # try:

    load_template = request.path.split('/')[-1]
    context['segment'] = load_template
    print(load_template)


    if load_template == 'gundem-dashboard.html':
        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["gundem"]).order_by('-pubDate')

    elif load_template == 'ekonomi-dashboard.html':

        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["borsa","Borsa", "analiz"]).order_by(
            '-pubDate')



    elif load_template == 'yasam-dashboard.html':
        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["yasam"]).order_by('-pubDate')

    elif load_template == 'spor-dashboard.html':
        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["spor"]).order_by('-pubDate')

    elif load_template == 'teknoloji-dashboard.html':
        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["teknoloji"]).order_by('-pubDate')

    elif load_template == 'otomobil-dashboard.html':
        context['queryset'] = news.objects.all().filter(Q(is_admin=True) | Q(is_editor=True)).filter(category__in=["otomobil"]).order_by('-pubDate')

    # for q in context['queryset']:
    #     print(q.user.first())
    html_template = loader.get_template(load_template)
    return HttpResponse(html_template.render(request=request, context=context))

    # except template.TemplateDoesNotExist:

        # html_template = loader.get_template('page-404.html')
        # return HttpResponse(html_template.render(context, request))

    # except:
    #
    #     html_template = loader.get_template('page-500.html')
    #     return HttpResponse(html_template.render(context, request))
