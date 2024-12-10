from time import sleep

from celery import shared_task
from api.models import Payment, Order
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail


@shared_task
def send_wishlist_email(user_email, product_name):
    send_mail(
        subject="Wishlist Update",
        message=f"The product '{product_name}' has been added to your wishlist.",
        from_email="noreply@yourshop.com",
        recipient_list=[user_email],
    )