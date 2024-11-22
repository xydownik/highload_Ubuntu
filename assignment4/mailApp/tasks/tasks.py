from __future__ import absolute_import, unicode_literals

import csv

from celery import shared_task
from django.core.mail import send_mail

from .models import Email, UploadedFile


@shared_task
def hello():
    return 'Hello World!'
@shared_task
def add(x, y):
    return x + y

@shared_task(bind=True, max_retries=3)
def send_email_task(self, email_id):
    try:
        email_obj = Email.objects.get(id=email_id)
        send_mail(
            email_obj.subject,
            email_obj.body,
            'from@example.com',
            [email_obj.recipient],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
@shared_task(bind=True, max_retries=3)
def process_file(self, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        with open(uploaded_file.file.path, 'r') as f:
            reader = csv.reader(f)
            # Simulate data processing
            total_rows = sum(1 for row in reader)
            f.seek(0)  # Reset file pointer
            for i, row in enumerate(reader):
                # Simulate processing each row
                uploaded_file.progress = (i + 1) / total_rows * 100
                uploaded_file.save()
        uploaded_file.processed = True
        uploaded_file.save()
    except Exception as exc:
        self.retry(exc=exc)