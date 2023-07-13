import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from Posts.models import Post, Category

logger = logging.getLogger(__name__)


def my_job():
    only_article = Post.objects.filter(article_or_news__istartswith="AT").dates("datetime", "week").values()[:3]

    choose_category = 0
    category_number = Category.objects.all().values()[choose_category]["id"]
    category_name = Category.objects.all().values()[category_number - 1]["name_category"]

    get_emails = list(User.objects.filter(subscriptions__category=category_number).values_list('email', flat=True))

    for email in get_emails:
        send_mail(
            subject=f'Новый список статей из категории {category_name}',
            message='\n'.join(['{} - {} http://127.0.0.1:8000/articles/{}'.format(
                _content["header"][:10] + "...",
                _content["text"][:30] + "...",
                _content["id"]) for _content in only_article]),
            from_email=None,
            recipient_list=[email],
        )


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="00 18 * * 5"),  # В 18:00 пятницу.
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
