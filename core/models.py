from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import *


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(max_length=200, unique=True)
    address = models.TextField(null=True)
    phone = models.BigIntegerField(null=True)

    is_manager = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return self.email
    

class ValidEmail(models.Model):
    email = models.EmailField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField() 

class InvalidEmail(models.Model):
    email = models.EmailField()
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField()        
