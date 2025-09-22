from django.contrib.auth.models import User
from django.db import models

class UserOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secret = models.CharField(max_length=32, blank=True, null=True)