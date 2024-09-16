from django.db import models


class User(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_subscribed = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
