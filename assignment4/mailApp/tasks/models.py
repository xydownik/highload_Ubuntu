from django.db import models

# Create your models here.

class Email(models.Model):
    recipient = models.EmailField(verbose_name='recipient')
    subject = models.CharField(max_length=255,verbose_name='subject')
    body = models.TextField(verbose_name='body')
    sent = models.BooleanField(default=False)

    def __str__(self):
        return self.subject