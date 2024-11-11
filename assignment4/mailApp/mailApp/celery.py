from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailApp.settings')

app = Celery('mailApp')

# Load configuration from Django settings, using the 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks from installed apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')