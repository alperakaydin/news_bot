from django.contrib import admin
from news.models import news, company_news, source_data, settings,video_source
admin.site.register(news)
admin.site.register(company_news)
admin.site.register(source_data)
admin.site.register(settings)
admin.site.register(video_source)
