import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')


import pytest
from django.contrib.auth import get_user_model
from api.models import Product, ShoppingCart, CartItem, Order, OrderItem, Category

User = get_user_model()

@pytest.mark.django_db
def test_add_product_to_cart():
    category = Category.objects.create(name='Test Category1', parent_id=1)
    user = User.objects.create_user(username='testuser', email= 'test@gmail.com', password='testpass', first_name='firstname', last_name='lastname')
    product = Product.objects.create(name='Test Product', price=100.00, stock_quantity=10, category_id=category)
    cart = ShoppingCart.objects.create(user_id=user)
    cart_item = CartItem.objects.create(cart_id=cart, product_id=product, quantity=2)

    assert cart_item.cart_id == cart
    assert cart_item.product_id == product
    assert cart_item.quantity == 2

@pytest.mark.django_db
def test_create_order_from_cart():
    category = Category.objects.create(name='Test Category2', parent_id=1)
    user = User.objects.create_user(username='testuser', email= 'test@gmail.com', password='testpass', first_name='firstname', last_name='lastname')
    product = Product.objects.create(name='Test Product', price=100.00, stock_quantity=10, category_id=category)
    cart = ShoppingCart.objects.create(user_id=user)
    CartItem.objects.create(cart_id=cart, product_id=product, quantity=2)

    order = Order.objects.create(user_id=user, order_status='Pending', total_amount=200.00)
    OrderItem.objects.create(order_id=order, product_id=product, quantity=2, price=100.00)

    assert order.user_id == user
    assert order.order_status == 'Pending'
    assert order.total_amount == 200.00

@pytest.mark.django_db
def test_payment_for_order():
    user = User.objects.create_user(username='testuser', email= 'test@gmail.com', password='testpass', first_name='firstname', last_name='lastname')
    order = Order.objects.create(user_id=user, order_status='Pending', total_amount=200.00)

    # Simulate payment logic
    order.order_status = 'Completed'
    order.save()

    assert order.order_status == 'Completed'
