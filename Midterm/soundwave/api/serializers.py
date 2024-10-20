from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'password']

    def create(self, validated_data):
        # Create a new user and hash the password
        user = User(
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'user']

    def create(self, validated_data):
        return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True)
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'orderItems', 'total', 'user']

    def create(self, validated_data):
        order_items_data = validated_data.pop('orderItems')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            order_item = OrderItem.objects.create(**item_data)
            order.orderItems.add(order_item)

        return order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


