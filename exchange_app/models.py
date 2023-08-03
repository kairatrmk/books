from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractBaseUser):
    email = models.EmailField(db_index=True, unique=True, blank=False, null=False, verbose_name='Email')
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='First Name')
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Last Name')
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name='Phone Number')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='Password')
    city = models.CharField(max_length=155, blank=True, null=True, verbose_name='Город')
    country = models.CharField(max_length=155, blank=True, null=True, verbose_name='Страна')


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


User = get_user_model()

class Book(models.Model):
    available = models.BooleanField(default=True, verbose_name='В наличии', help_text='Отметьте, если книга доступна для выдачи')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genr = models.ForeignKey('Genre', on_delete=models.PROTECT, null=True)
    condition = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name="books", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='book_photos/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class Genre(models.Model):
    name=models.CharField(max_length=155, db_index=True)

    def __str__(self):
        return self.name
