from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.utils.html import escape
from encrypted_model_fields.fields import EncryptedEmailField, EncryptedCharField
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
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField( default=0)
    email = EncryptedEmailField(unique=True)
    telegram_account = models.URLField(validators=[URLValidator()], default=0)
    description = models.TextField(default='', verbose_name='description')
    UIN = EncryptedCharField(max_length=12, default= 'No UIN')


    def save(self, *args, **kwargs):
        self.description = escape(self.description)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class UploadedFile(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    progress = models.FloatField(default=0.0)