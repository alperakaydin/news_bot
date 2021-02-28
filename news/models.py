from django.db import models

class news(models.Model):
    source = models.CharField(max_length=200, verbose_name="Kaynak", blank="",null=True)
    title = models.CharField(max_length=200, verbose_name="Başlık",null=True)
    category = models.CharField(max_length=200, verbose_name="Kategori", blank="" ,null=True)
    subcategory = models.CharField(max_length=200, verbose_name="Alt Kategori", blank="",null=True)
    description = models.TextField( verbose_name="Özet", blank="",null=True)
    pubDate = models.DateTimeField( verbose_name="Yayınlanma Tarihi", blank="",null=True)
    link = models.URLField( verbose_name="Haber Link", unique=True)
    thumbnail_url = models.URLField( verbose_name="Resim Link", blank="",null=True)
    is_favorite = models.BooleanField(blank=False, verbose_name="Favori",null=True)
    is_select = models.BooleanField(blank=False, verbose_name="Seç",null=True)

