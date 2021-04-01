from django.db import models
from django.contrib.auth.models import User


class news(models.Model):
    source = models.CharField(max_length=200, verbose_name="Kaynak", blank="", null=True)
    title = models.CharField(max_length=200, verbose_name="Başlık", null=True)
    category = models.CharField(max_length=200, verbose_name="Kategori", blank="", null=True)
    subcategory = models.CharField(max_length=200, verbose_name="Alt Kategori", blank="", null=True)
    description = models.TextField(verbose_name="Özet", blank="", null=True)
    pubDate = models.DateTimeField(verbose_name="Yayınlanma Tarihi", blank="", null=True)
    link = models.URLField(verbose_name="Haber Link", unique=True)
    thumbnail_url = models.URLField(verbose_name="Resim Link", blank="", null=True)
    is_admin = models.BooleanField(blank=False, default=False, null=True, verbose_name="Admin")  # is_admin yap
    is_editor = models.BooleanField(blank=False, default=False, null=True, verbose_name="Editor")  # is_editor
    is_video = models.BooleanField(blank=False, default=False, null=True, verbose_name="Video")
    is_company_news = models.BooleanField(blank=False, default=False, null=True, verbose_name="Şirket")
    company_code = models.CharField(max_length=50, verbose_name="Şirket Kodu", null=True)
    extra_field = models.TextField(verbose_name="Extra Alan", blank="", null=True)
    # user = models.ForeignKey(User,related_name='selected_news', related_query_name='haber',null=True, on_delete=models.CASCADE )
    user = models.ManyToManyField(User, related_name='selected_news', related_query_name='haber')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Haber'
        verbose_name_plural = 'Haberler'


class video_source(models.Model):
    CATEGORY_CHOICES = [
        ("borsa", "Borsa"),
        ("yasam", "Yaşam"),
        ("spor", "Spor"),
        ("otomobil", "Otomobil"),
        ("teknoloji", "Teknoloji"),
    ]
    category = models.CharField(max_length=12, choices=CATEGORY_CHOICES, verbose_name="Kategori", unique=True)
    url = models.URLField(verbose_name="Kaynak Url", unique=True)
    javascript_content = models.TextField(verbose_name="JavaScript", null=True)
    html_content = models.TextField(verbose_name="HTML", null=True)


class company_news(models.Model):
    MedalType = models.TextChoices('MedalType', 'GOLD SILVER BRONZE')
    deneme = models.TextChoices('deneme', 'birinci ikinci ucuncu')
    source = models.CharField(max_length=200, verbose_name="Kaynak", blank="", null=True)
    html_content = models.TextField(verbose_name="Html İçerik", blank="", null=True)
    pubDate = models.DateTimeField(verbose_name="Yayınlanma Tarihi", blank="", null=True)

    class Meta:
        verbose_name = 'Şirket Haberi'
        verbose_name_plural = 'Şirket Haberleri'


class source_data(models.Model):
    source_name = models.CharField(max_length=200, verbose_name="Kaynak Adı", null=True)
    url = models.URLField(verbose_name="Kaynak Url", unique=True)
    CATEGORY_CHOICES = [
        ("borsa", "Borsa"),
        ("gundem", "Gündem"),
        ("yasam", "Yaşam"),
        ("spor", "Spor"),
        ("otomobil", "Otomobil"),
        ("teknoloji", "Teknoloji"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategori", null=True)
    # subcategory = models.CharField(max_length=200, verbose_name="Alt Kategori", null=True)
    time_code = models.IntegerField(verbose_name="Zaman Farkı", null=True, default=3)
    permission_count = models.IntegerField(verbose_name="Kaç Haber Alınabilir", null=True, default=3)
    # special_code = models.IntegerField(verbose_name="Resim İşleme Kodu", null=True)
    active = models.BooleanField(blank=True, verbose_name="Aktif", null=True, default=True)
    is_youtube = models.BooleanField(blank=False, verbose_name="Youtube", null=True)

    # refresh_time = models.IntegerField(verbose_name="Yenilenme Zamanı", null=True)
    def __str__(self):
        return self.source_name + "  -  " + self.category

    class Meta:
        verbose_name = 'Kaynak Veri'
        verbose_name_plural = 'Kaynak Verileri'


class settings(models.Model):
    refresh_time = models.IntegerField(verbose_name="Yenilenme Zamanı", null=True)
    uptime = models.IntegerField(verbose_name="Güncel Kalma Süresi", null=True)
    proxies = models.TextField(verbose_name="proxies", default=None, null=True)
    headers = models.TextField(verbose_name="headers", default=None, null=True)
    frequency = models.IntegerField(verbose_name="Çalışma Frekansı", default=120, null=True)
    max_thread = models.IntegerField(verbose_name="Maksimum İşlemçi Sayısı", default=1, null=True)

    class Meta:
        verbose_name = 'Ayar'
        verbose_name_plural = 'Ayarlar'
