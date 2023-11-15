from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('Counselor', 'Counselor'),
        ('Parent', 'Parent'),
        ('Teacher', 'Teacher'),
        ('IT Admin', 'IT Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
