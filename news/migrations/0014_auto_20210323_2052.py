# Generated by Django 3.1.7 on 2021-03-23 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0013_auto_20210323_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='user',
        ),
        migrations.AddField(
            model_name='news',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='selected_news', related_query_name='haber', to=settings.AUTH_USER_MODEL),
        ),
    ]
