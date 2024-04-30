from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)  # using their registered email address as their unique identifier
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000.00)
    currency = models.CharField(max_length=3, default="GBP")
