import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_platform.settings')

app = Celery('trade_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'UTC'
