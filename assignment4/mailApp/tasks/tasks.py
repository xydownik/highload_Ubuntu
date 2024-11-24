from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from .models import Email
import csv
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from .models import UploadedFile
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
def process_file(self, uploaded_file_id):
    try:
        uploaded_file = get_object_or_404(UploadedFile, id=uploaded_file_id)
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            f"user_{uploaded_file.user.id}_progress",
            {"type": "send_progress", "progress": 0, "message": "Processing started"},
        )

        with open(uploaded_file.file.path, "r") as file:
            reader = csv.reader(file)
            total_rows = sum(1 for _ in reader)
            file.seek(0)

            for i, row in enumerate(reader):
                progress = int((i + 1) / total_rows * 100)
                async_to_sync(channel_layer.group_send)(
                    f"user_{uploaded_file.user.id}_progress",
                    {"type": "send_progress", "progress": progress, "message": f"Processing row {i + 1}/{total_rows}"},
                )

        async_to_sync(channel_layer.group_send)(
            f"user_{uploaded_file.user.id}_progress",
            {"type": "send_progress", "progress": 100, "message": "Processing completed"},
        )

    except Exception as exc:
        async_to_sync(channel_layer.group_send)(
            f"user_{uploaded_file.user.id}_progress",
            {"type": "send_progress", "progress": 0, "message": f"Error: {str(exc)}"},
        )
        self.retry(exc=exc)
