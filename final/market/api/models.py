from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.timezone import now

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set.")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['email']),  # Indexing email for faster lookups
            models.Index(fields=['username']),  # Indexing username for faster lookups
        ]

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_id = models.IntegerField()
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Indexing category name for filtering
            models.Index(fields=['parent_id']),  # Indexing parent_id for faster lookups
        ]

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='No description')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Indexing product name for faster search
            models.Index(fields=['category_id']),  # Indexing category_id for filtering
            models.Index(fields=['price']),  # Indexing price for filtering or sorting
        ]

class Order(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_status

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),  # Indexing user_id for filtering
            models.Index(fields=['order_status']),  # Indexing order status for faster lookups
        ]

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id} - {self.product_id}"

    class Meta:
        indexes = [
            models.Index(fields=['order_id', 'product_id']),  # Composite index for fast lookups
        ]

class ShoppingCart(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),  # Indexing user_id for filtering
        ]

class CartItem(models.Model):
    cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id} - {self.product_id}"

    class Meta:
        indexes = [
            models.Index(fields=['cart_id', 'product_id']),  # Composite index for fast lookups
        ]


class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        indexes = [
            models.Index(fields=['product_id']),  # Indexing product_id for filtering reviews by product
            models.Index(fields=['user_id']),  # Indexing user_id for filtering reviews by user
            models.Index(fields=['rating']),  # Indexing rating for fast lookups
        ]

class Wishlist(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),  # Indexing user_id for filtering by user
        ]

class WishlistItem(models.Model):
    wishlist_id = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.wishlist_id} - {self.product_id}"

    class Meta:
        indexes = [
            models.Index(fields=['wishlist_id', 'product_id']),  # Composite index for fast lookups
        ]
