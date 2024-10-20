
import pytest
from django.urls import reverse
from soundwave.api.models import Order, Product

@pytest.mark.django_db
def test_create_order():
    product = Product.objects.create(price=20.0)
    response = client.post(reverse('order-create'), {'items': [{'product_id': product.id, 'quantity': 3}]})
    assert response.status_code == 201
    assert Order.objects.count() == 1
    assert Order.objects.first().total() == 60.0
