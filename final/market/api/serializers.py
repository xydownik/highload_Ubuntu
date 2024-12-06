from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent_id', 'created_at', 'updated_at']

class ProductSerializer(serializers.ModelSerializer):
    category_id = CategorySerializer()
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock_quantity', 'category_id', 'created_at', 'updated_at']

class OrderSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'order_status', 'total_amount', 'created_at', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    product_id = ProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order_id', 'product_id', 'quantity', 'price', 'created_at', 'updated_at']

class ShoppingCartSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()
    class Meta:
        model = ShoppingCart
        fields = ['id', 'user_id', 'created_at', 'updated_at']

class CartItemSerializer(serializers.ModelSerializer):
    cart_id = ShoppingCartSerializer()
    product_id = ProductSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'cart_id', 'product_id', 'quantity', 'created_at', 'updated_at']

class PaymentSerializer(serializers.ModelSerializer):
    order_id = OrderSerializer()
    class Meta:
        model = Payment
        fields = ['id', 'order_id', 'payment_method', 'amount', 'status', 'created_at', 'updated_at']

class ReviewSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer()
    user_id = CustomUserSerializer()
    class Meta:
        model = Review
        fields = ['id', 'product_id', 'user_id', 'rating', 'comment', 'created_at', 'updated_at']

class WishlistSerializer(serializers.ModelSerializer):
    user_id = CustomUserSerializer()
    class Meta:
        model = Wishlist
        fields = ['id', 'user_id', 'created_at', 'updated_at']

class WishlistItemSerializer(serializers.ModelSerializer):
    wishlist_id = WishlistSerializer()
    product_id = ProductSerializer()
    class Meta:
        model = WishlistItem
        fields = ['id', 'wishlist_id', 'product_id', 'created_at']
