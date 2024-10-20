# tasks.py

from celery import shared_task

from api.models import Order


@shared_task
def process_order(order_id):
    try:
        order = Order.objects.get(id=order_id)

        charge_payment(order)
        update_stock(order)

        print(f"Order {order.id} processed successfully.")
    except Order.DoesNotExist:
        print(f"Order with id {order_id} does not exist.")
    except Exception as e:
        print(f"Error processing order {order_id}: {e}")


def charge_payment(order):
    total_amount = 0

    for order_item in order.orderItems.all():
        total_amount += order_item.product.price * order_item.quantity

    order.total = total_amount
    order.save()

    print(f"Total amount for order {order.id} calculated as {order.total}.")


def update_stock(order):
    for order_item in order.orderItems.all():
        product = order_item.product
        product.stock -= order_item.quantity
        product.save()
    print(f"Updating stock for order {order.id}.")

