# Asynchronous Processing in E-Commerce Platform

Asynchronous processing is a crucial aspect of modern web applications, especially in an e-commerce platform where operations like payment processing, order management, and email notifications can be time-consuming. By offloading these tasks to background workers, we can improve the responsiveness and scalability of the platform.

This document describes the implementation of asynchronous tasks using **Celery**, focusing on the payment processing and order confirmation email features.

## Table of Contents

1. [Introduction](#introduction)
2. [Celery Integration](#celery-integration)
    - [Task: `process_payment`](#task-process_payment)
    - [Task: `send_order_confirmation_email`](#task-send_order_confirmation_email)
3. [Views for Handling Orders](#views-for-handling-orders)
    - [View: `view_order`](#view-view_order)
    - [View: `pay_order`](#view-pay_order)
    - [View: `order_success`](#view-order_success)
4. [Payment Model](#payment-model)
5. [Conclusion](#conclusion)

---

## Introduction

In a distributed e-commerce system, operations like payment processing can take significant time, especially when dealing with external payment gateways. To avoid blocking the user interface or overloading the server, these tasks should be offloaded to asynchronous background workers.

In this system, we are using **Celery** to handle such tasks asynchronously, allowing the main application to remain responsive while the heavy lifting is done in the background.

## Celery Integration

Celery is a distributed task queue system that allows you to run long-running tasks asynchronously in the background. Below is how we integrate Celery into the platform.

### Task: `process_payment`

The `process_payment` task handles the payment processing asynchronously. Once a payment is initiated, the task will:

1. Connect to the **Cassandra** database to retrieve and update the payment status.
2. Mark the payment as **Completed** once processed.

```python
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
        return f"Error processing payment: {str(e)}"
```
This task is triggered when a payment is successfully created in the system, and it updates the payment status asynchronously.

## Task: send_order_confirmation_email
The `send_order_confirmation_email` task is responsible for sending an email notification to the user after an order is placed. This task is performed asynchronously to avoid blocking the main application.

```python
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
```
Once the order is confirmed, this task sends an email to the user confirming the order details.

## Views for Handling Orders
The views handle the creation of orders and the initiation of payment. These views also trigger the asynchronous tasks.

### View: `view_order`
This view retrieves the cart from the session, calculates the total amount, and creates a new order.

```python
@login_required
def view_order(request):
    # Get the cart from the session
    cart = request.session.get('cart', {})

    # Calculate total amount
    total_amount = sum(item['price'] * item['quantity'] for item in cart.values())

    # Create a new order
    order = Order.objects.create(
        user_id=request.user,
        total_amount=total_amount,
        order_status="Pending"  # Default order status
    )

    # Add items to the order
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        OrderItem.objects.create(
            order_id=order,
            product_id=product,
            quantity=item['quantity'],
            price=item['price']
        )

    # Show order review page
    return render(request, 'pay/order_review.html', {'order': order, 'total_amount': total_amount})
```
This view is responsible for presenting the user with an order review page before proceeding to payment.

### View: `pay_order`
This view handles the payment process. After the user submits the payment form, it creates a Payment record and triggers the process_payment and send_order_confirmation_email tasks.

```python
@login_required
def pay_order(request, order_id):
    # Get the order
    order = get_object_or_404(Order, id=order_id, user_id=request.user)
    order_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(order.id))
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Create a payment record
            payment = Payment.objects.using('my_keyspace').create(
                order_id=order_uuid,
                payment_method=form.cleaned_data['payment_method'],
                amount=order.total_amount,
                status="Pending"
            )

            payment.save()
            order.status = "Completed"
            # Trigger background tasks for payment processing and email confirmation
            process_payment.delay(payment.id)
            send_order_confirmation_email.delay(order.id)

            return redirect('order_success')
    else:
        form = PaymentForm()

    return render(request, 'pay/payment_form.html', {'form': form, 'order': order})
```
This view creates the payment and triggers the asynchronous tasks that handle payment processing and email notifications.

### View: `order_success`
This view displays a success message once the payment has been processed and the email is sent.

```python
@login_required
def order_success(request):
    return render(request, 'pay/order_success.html')
```
Payment Model
The Payment model represents the payment information in the system. It uses Cassandra for high availability and scalability in handling payment data.

```python
from cassandra.cqlengine.models import Model
from cassandra.cqlengine.columns import UUID, Decimal, Text, DateTime
import uuid
from datetime import datetime

class Payment(Model):
    __table_name__ = 'payment'

    id = UUID(primary_key=True, default=uuid.uuid4)
    order_id = UUID(index=True)  # Secondary index for order_id
    payment_method = Text()
    amount = Decimal()
    status = Text(index=True)  # Secondary index for status
    created_at = DateTime(default=datetime.now)
    updated_at = DateTime(default=datetime.now)
```
The Payment model is used to store payment information in the Cassandra database.

Conclusion
Asynchronous processing in e-commerce platforms significantly enhances the user experience by ensuring that long-running tasks like payment processing and email notifications do not block the main application. By integrating Celery for background task execution and using Cassandra for payment storage, this platform efficiently handles high volumes of transactions and notifications, improving both scalability and performance.



