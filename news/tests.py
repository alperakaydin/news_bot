from django.test import TestCase

# Create your tests here.
from news.models import news


queryset = news.objects.first()
print(queryset)