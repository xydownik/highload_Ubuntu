# tasks.py
from uuid import UUID

from cassandra.cluster import Cluster
from celery import shared_task
from django.core.mail import send_mail
from api.models import Order

from .models import Payment
from market import settings


@shared_task
def process_payment(payment_id):
    try:
        # Access Cassandra settings directly from Django's settings
        cassandra_settings = settings.DATABASES['cassandra']
        host = cassandra_settings['HOST']
        port = cassandra_settings['PORT']
        keyspace = cassandra_settings['NAME']

        # Manually connect to Cassandra using the settings
        cluster = Cluster([host], port=port)
        session = cluster.connect(keyspace)

        # Retrieve the payment from Cassandra database
        payment = Payment.objects.using('my_keyspace').get(id=payment_id)
        payment.status = "Completed"
        payment.save()

        return "Payment processed successfully"

    except Payment.DoesNotExist:
        return f"Payment with ID {payment_id} not found"

    except Exception as e:
        # Log or handle any other exceptions
        return f"Error processing payment: {str(e)}"
@shared_task
def send_order_confirmation_email(order_id):
    order = Order.objects.get(id=order_id)
    user_email = order.user_id.email
    send_mail(
        'Order Confirmation',
        f'Your order #{order.id} has been confirmed.',
        'no-reply@example.com',
        [user_email],
        fail_silently=False,
    )
    return True
