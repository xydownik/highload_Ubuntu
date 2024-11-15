from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.utils.html import escape
# Create your models here.

class Email(models.Model):
    sender = models.EmailField(verbose_name='sender', max_length=254, default= 'unknown@gmail.com')
    recipient = models.EmailField(verbose_name='recipient')
    subject = models.CharField(max_length=255,verbose_name='subject')
    body = models.TextField(verbose_name='body')
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure emails are unique

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField( default=0)
    email = models.EmailField()
    telegram_account = models.URLField(validators=[URLValidator()], default=0)
    description = models.TextField(default='', verbose_name='description')

    def save(self, *args, **kwargs):
        self.description = escape(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name