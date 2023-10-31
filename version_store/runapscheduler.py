# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# İCRAWLER
from crochet import setup

from icrawler import scrapy_tasks
# İCRAWLER


logger = logging.getLogger(__name__)
from _rss_bundler import rss2

def rss_shedule_job():
    #  Your job processing logic here...
    # setup()
    print("rss_shedule_job")
    rss2.run_rss_schedular()
    # print("Ben Çalışıyorum uhuhuuuhuuuuuuuu......")

def scrapy_shedule_job():

    # setup()
    print("scrapy_shedule_job")
    s = scrapy_tasks.Scraper()

    s.run_spiders()
    print("Ben Çalışıyorum uhuhuuuhuuuuuuuu......")

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):

        # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            rss_shedule_job,
            trigger=CronTrigger(minute="*/2"),  # Every 10 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'rss_shedule_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

    def handle_scrapy(self, *args, **options):

            # scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
            scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
            scheduler.add_jobstore(DjangoJobStore(), "default")

            scheduler.add_job(
                scrapy_shedule_job,
                trigger=CronTrigger(minute="*/10"),  # Every 10 seconds
                id="my_job2",  # The `id` assigned to each job MUST be unique
                max_instances=1,
                replace_existing=True,
            )
            logger.info("Added job 'scrapy_shedule_job'.")

            scheduler.add_job(
                delete_old_job_executions,
                trigger=CronTrigger(
                    day_of_week="mon", hour="00", minute="00"
                ),  # Midnight on Monday, before start of the next work week.
                id="delete_old_job_executions",
                max_instances=1,
                replace_existing=True,
            )
            logger.info(
                "Added weekly job: 'delete_old_job_executions'."
            )

            try:
                logger.info("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                logger.info("Stopping scheduler...")
                scheduler.shutdown()
                logger.info("Scheduler shut down successfully!")

