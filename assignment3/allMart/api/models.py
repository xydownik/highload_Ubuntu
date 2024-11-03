from django.db import models

# Create your models here.

class KeyValue(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.key
