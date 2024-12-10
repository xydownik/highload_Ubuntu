# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from api.models import Payment, Order

@shared_task
def process_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    # Логика обработки платежа (например, через API стороннего платежного провайдера)
    payment.status = "Completed"
    payment.save()
    return True

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
