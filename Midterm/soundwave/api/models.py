from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=200, db_index=True)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description")
    def __str__(self):
        return self.name

class User(AbstractUser):
    phone_number=models.CharField(max_length=15)
    def __str__(self):
        return self.username

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
class Order(models.Model):
    orderItems = models.ManyToManyField(OrderItem, default= None)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    def __str__(self):
        return self.user.name




