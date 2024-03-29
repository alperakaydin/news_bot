# Generated by Django 3.1.7 on 2021-03-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_auto_20210320_2310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source_data',
            name='is_youtube',
        ),
        migrations.RemoveField(
            model_name='source_data',
            name='refresh_time',
        ),
        migrations.AlterField(
            model_name='source_data',
            name='active',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Aktif'),
        ),
        migrations.AlterField(
            model_name='source_data',
            name='time_code',
            field=models.IntegerField(default=3, null=True, verbose_name='Zaman Farkı'),
        ),
    ]
