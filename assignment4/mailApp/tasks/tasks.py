from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail

from .models import Email


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
            'from@example.com',  # replace with a valid sender email
            [email_obj.recipient],
            fail_silently=False,
        )
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)