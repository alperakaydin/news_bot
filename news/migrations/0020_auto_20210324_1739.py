# Generated by Django 3.1.7 on 2021-03-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0019_auto_20210324_0022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='is_favorite',
        ),
        migrations.RemoveField(
            model_name='news',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='news',
            name='is_admin',
            field=models.BooleanField(default=False, null=True, verbose_name='Admin'),
        ),
        migrations.AddField(
            model_name='news',
            name='is_editor',
            field=models.BooleanField(default=False, null=True, verbose_name='Editor'),
        ),
    ]