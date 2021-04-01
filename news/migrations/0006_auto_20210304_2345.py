# Generated by Django 3.1.7 on 2021-03-04 23:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0005_news_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='user',
            field=models.ManyToManyField(related_name='selected_news', related_query_name='haber', to=settings.AUTH_USER_MODEL),
        ),
    ]