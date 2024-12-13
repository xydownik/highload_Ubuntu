# views.py
import uuid

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from api.models import Order, OrderItem, Product
from django.views.decorators.cache import cache_page

from .forms import PaymentForm
from .models import Payment
from .tasks import process_payment, send_order_confirmation_email


@login_required
def view_order(request):
    # Достаём корзину из сессии
    cart = request.session.get('cart', {})

    # Вычисляем общую сумму
    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())

    # Создаём новый заказ
    order = Order.objects.create(
        user_id=request.user,
        total_amount=total_amount,
        order_status="Pending"  # Статус заказа по умолчанию
    )

    # Добавляем товары в заказ
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(
            order_id=order,
            product_id=product,
            quantity=item['quantity'],
            price=item['price']
        )

    # Отображаем страницу подтверждения заказа
    return render(request, 'pay/order_review.html', {'order': order, 'total_amount': total_amount})


@login_required
def pay_order(request, order_id):
    # Получаем заказ
    order = get_object_or_404(Order, id=order_id, user_id=request.user)
    order_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(order.id))
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Создаём запись платежа
            payment = Payment.objects.using('my_keyspace').create(
                order_id=order_uuid,
                payment_method=form.cleaned_data['payment_method'],
                amount=order.total_amount,
                status="Pending"
            )

            payment.save()
            order.status = "Completed"
            # Запуск фоновых задач для обработки платежа и отправки письма
            process_payment.delay(payment.id)
            send_order_confirmation_email.delay(order.id)

            return redirect('order_success')
    else:
        form = PaymentForm()

    return render(request, 'pay/payment_form.html', {'form': form, 'order': order})


@login_required
def order_success(request):
    return render(request, 'pay/order_success.html')
