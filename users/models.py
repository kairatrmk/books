from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    email = models.EmailField(db_index=True, unique=True, blank=False, null=False, verbose_name='Email')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Phone Number')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Password')
    city = models.CharField(max_length=155, blank=True, null=True, verbose_name='Город')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
