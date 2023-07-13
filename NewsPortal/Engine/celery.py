import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Engine.settings')

app = Celery('Engine')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Задание cron, которое запускается каждый понедельник в 8 утра.
app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'Cron.tasks.send_last_news',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}
