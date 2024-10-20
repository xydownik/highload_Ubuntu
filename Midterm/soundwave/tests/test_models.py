
import pytest
from soundwave.api.models import *

@pytest.mark.django_db
def test_order_total_calculation():
    product1 = Product.objects.create(price=10.0)
    product2 = Product.objects.create(price=5.0)
    order = Order()
    order.items.add(OrderItem(product=product1, quantity=2))
    order.items.add(OrderItem(product=product2, quantity=1))
    assert order.total() == 25.0
