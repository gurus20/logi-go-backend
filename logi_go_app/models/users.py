from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Role(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    country = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    phone_country_code = models.CharField(max_length=10)
    phone_verified = models.BooleanField(default=False)
    support_email = models.EmailField()
    email_verified = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.user.username or self.user.email
    
