# Generated by Django 3.1.7 on 2021-02-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_auto_20210221_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='link',
            field=models.URLField(blank='', null=True, unique=True, verbose_name='Haber Link'),
        ),
    ]
