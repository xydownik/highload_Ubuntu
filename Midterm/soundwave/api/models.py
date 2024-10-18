from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(default="No description")
    def __str__(self):
        return self.name

class User(AbstractUser):
    phone_number=models.CharField(max_length=15)
    def __str__(self):
        return self.username

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self