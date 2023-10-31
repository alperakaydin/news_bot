import os
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_bot.settings")
import django
django.setup()
from news.models import news,User

def periodic_database_cleaner(frequency_day=7):
    print(" FREQUENCY :: ",frequency_day)
    today = datetime.now()
    last_week = today - timedelta(days=frequency_day)

    # Seçilmemiş haberler
    not_selected_old_news = news.objects.all().filter(pubDate__lt=last_week).filter(is_editor=False).filter(is_admin=False).order_by("pubDate")
    for n in not_selected_old_news:
        # user = n.user
        # q = User.objects.get(username=user.name)
        print("DELETED :\t", n.title )
        # n.user.remove(user.id)
        n.delete()

        pass
    # haber.user.remove(user)

    editor_selected_old_news = news.objects.all().filter(pubDate__lt=last_week).filter(is_editor=True).order_by("pubDate")

    for n in editor_selected_old_news:
        users = n.user.all()
        for user in users:
            n.user.remove(user.id)
            print("DELETE İS OK!   :username:" ,user.username)

        print(n.title,"    :     ",users)
        print("News was deleted..  :id: ", n.id)
        n.delete()

    admin_selected_old_news = news.objects.all().filter(pubDate__lt=last_week).filter(is_admin=True).order_by("pubDate")

    for n in admin_selected_old_news:
        users = n.user.all()
        for user in users:
            n.user.remove(user.id)
            print("DELETE İS OK!   :username:", user.username)

        print(n.title, "    :     ", users)
        print("News was deleted..  :id: ", n.id)
        n.delete()


if __name__ == '__main__':
    periodic_database_cleaner()
    # q = User.objects.all()
    # print(q)


    # TODO Çorumda burada kaldım :)